from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'meurhunivag' # Mantenha sua chave secreta aqui

# Adicione mais usuários conforme necessário
USUARIOS = {
    'rh': {'senha': 'rh123', 'tipo': 'rh'},
    'hianny': {'senha': '123', 'tipo': 'funcionario', 'id': 1},
    'joao': {'senha': '123', 'tipo': 'funcionario', 'id': 2},
    'maria': {'senha': '123', 'tipo': 'funcionario', 'id': 3}
}

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d/%m/%Y'):
    if pd.isna(value) or value == '':
        return "N/A"
    try:
        # Tenta converter de string para datetime antes de formatar
        if isinstance(value, str):
            # Tenta formatos comuns, ajuste conforme a origem dos seus dados
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                try:
                    value = datetime.strptime(value, '%d/%m/%Y')
                except ValueError:
                    return value # Retorna o valor original se não conseguir parsear
        return value.strftime(format)
    except Exception:
        return value

@app.template_filter('currencyformat')
def currencyformat(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return value

@app.route('/')
def index():
    if 'username' in session:
        if session['tipo_usuario'] == 'rh':
            return redirect(url_for('painel_rh'))
        else:
            return redirect(url_for('painel_funcionario'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USUARIOS and USUARIOS[username]['senha'] == password:
            session['username'] = username
            session['tipo_usuario'] = USUARIOS[username]['tipo']
            
            if USUARIOS[username]['tipo'] == 'funcionario':
                session['funcionario_id'] = USUARIOS[username].get('id', 1)
                
                # Carrega os dados do funcionário do CSV e armazena na sessão
                try:
                    df_funcionarios = pd.read_csv(r'./UnivagRH/tests/static/csv/FuncionarioBase.csv', sep=';')
                    funcionario_data = df_funcionarios[df_funcionarios['ID'] == session['funcionario_id']].to_dict('records')
                    if funcionario_data:
                        session['funcionario_data'] = funcionario_data[0]
                    else:
                        session['funcionario_data'] = {} # Caso o ID não seja encontrado
                except Exception as e:
                    print(f"Erro ao carregar dados do funcionário do CSV: {e}")
                    session['funcionario_data'] = {}
                
                # Inicializa a lista de solicitações do funcionário na sessão (se não existir)
                if 'solicitacoes_funcionario_data' not in session:
                    session['solicitacoes_funcionario_data'] = [
                        # Exemplo de dados iniciais, em um app real viriam de um DB
                        {'tipo': 'Férias', 'data': '2024-03-01', 'status': 'Aprovado', 'observacao': 'Férias aprovadas para Março.'},
                        {'tipo': 'Atestado', 'data': '2024-04-10', 'status': 'Pendente', 'observacao': 'Aguardando validação do RH.'},
                        {'tipo': 'Declaração', 'data': '2024-02-20', 'status': 'Rejeitado', 'observacao': 'Documentação incompleta.'}
                    ]
            
            if USUARIOS[username]['tipo'] == 'rh':
                return redirect(url_for('painel_rh'))
            else:
                return redirect(url_for('painel_funcionario'))
        else:
            return render_template('login.html', erro="Usuário ou senha inválidos")
    
    return render_template('login.html')

@app.route('/rh')
def painel_rh():
    if 'username' not in session or session['tipo_usuario'] != 'rh':
        return redirect(url_for('login'))
    
    try:
        # Carrega dados do CSV (mantido como no seu código original)
        df = pd.read_csv(r'./UnivagRH/tests/static/csv/FuncionarioBase.csv', sep=';')
        
        # Processa solicitações (simulação - substitua por dados reais)
        solicitacoes = [
            {'funcionario': 'João Silva', 'tipo': 'Férias', 'data': '2023-06-15', 'status': 'Pendente'},
            {'funcionario': 'Maria Oliveira', 'tipo': 'Rescisão', 'data': '2023-05-20', 'status': 'Aprovado'},
            {'funcionario': 'Carlos Pereira', 'tipo': 'Banco de Horas', 'data': '2023-06-01', 'status': 'Rejeitado'}
        ]
        
        # Processa férias (calcula dias restantes)
        hoje = datetime.now().date()
        funcionarios_ferias = []
        
        for _, row in df.iterrows():
            try:
                data_ferias = datetime.strptime(str(row['ProximasFerias']), '%Y-%m-%d').date()
                dias_restantes = (data_ferias - hoje).days
                funcionario_data_rh = row.to_dict()
                funcionario_data_rh['dias_restantes'] = dias_restantes
                funcionarios_ferias.append(funcionario_data_rh)
            except Exception:
                continue # Ignora linhas com erro na data de férias
        
        # Ordena por proximidade das férias
        funcionarios_ferias.sort(key=lambda x: x['dias_restantes'])
        
        return render_template('rh.html', 
                               solicitacoes=solicitacoes,
                               funcionarios_ferias=funcionarios_ferias)
    
    except Exception as e:
        return f"Erro ao processar dados do RH: {str(e)}", 500

@app.route('/funcionario')
def painel_funcionario():
    if 'username' not in session or session['tipo_usuario'] != 'funcionario':
        return redirect(url_for('login'))
    
    # Pega os dados do funcionário e suas solicitações da sessão
    funcionario = session.get('funcionario_data', {})
    solicitacoes_funcionario = session.get('solicitacoes_funcionario_data', [])

    if not funcionario:
        return "Dados do funcionário não encontrados. Por favor, faça login novamente.", 404
    
    # Renderiza o template do dashboard do funcionário
    return render_template('funcionario.html', 
                           funcionario=funcionario,
                           solicitacoes_funcionario=solicitacoes_funcionario)

# *******************************************************************
# ** NOVA ROTA: Para a tela de criação de solicitação do funcionário **
# ** O HTML do botão "fazer uma nova solicitação aqui" deve apontar para esta rota: **
# ** <a href="/funcionarios/solicitacoes">fazer uma nova solicitação aqui</a> **
# *******************************************************************
@app.route('/funcionarios/solicitacoes', methods=['GET', 'POST'])
def criar_solicitacao_funcionario():
    if 'username' not in session or session['tipo_usuario'] != 'funcionario':
        return redirect(url_for('login'))

    funcionario = session.get('funcionario_data', {})
    if not funcionario:
        return "Dados do funcionário não disponíveis. Por favor, faça login novamente.", 400

    if request.method == 'GET':
        # Renderiza o formulário para criar uma nova solicitação
        return render_template('solicitacoes.html',
                               funcionario=funcionario)

    elif request.method == 'POST':
        tipo_solicitacao = request.form.get('requestType')
        data_solicitacao = request.form.get('requestDate')
        detalhes_solicitacao = request.form.get('requestDetails')

        # Validação básica dos campos
        if not all([tipo_solicitacao, data_solicitacao, detalhes_solicitacao]):
            # Em um cenário real, você renderizaria o formulário novamente com uma mensagem de erro
            return "Por favor, preencha todos os campos da solicitação.", 400

        # Adiciona a nova solicitação à lista na sessão
        # Em um app real, esta solicitação seria salva em um banco de dados
        solicitacoes_funcionario = session.get('solicitacoes_funcionario_data', [])
        solicitacoes_funcionario.append({
            'tipo': tipo_solicitacao,
            'data': data_solicitacao,
            'status': 'Pendente', # Nova solicitação sempre começa como Pendente
            'observacao': 'Sua solicitação foi recebida e está aguardando análise do RH.'
        })
        session['solicitacoes_funcionario_data'] = solicitacoes_funcionario # Atualiza a sessão

        # Após salvar, redireciona de volta para o painel do funcionário
        # para que ele possa ver a nova solicitação nas notificações
        return redirect(url_for('painel_funcionario'))

@app.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
