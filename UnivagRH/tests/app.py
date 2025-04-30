from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'meurhunivag'

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
        return datetime.strptime(str(value), '%Y-%m-%d').strftime(format)
    except:
        return value

@app.template_filter('currencyformat')
def currencyformat(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
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
        # Carrega dados do CSV
        df = pd.read_csv(fr'.\tests\static\csv\FuncionarioBase.csv', sep=';')
        
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
                data_ferias = datetime.strptime(row['ProximasFerias'], '%Y-%m-%d').date()
                dias_restantes = (data_ferias - hoje).days
                funcionario_data = row.to_dict()
                funcionario_data['dias_restantes'] = dias_restantes
                funcionarios_ferias.append(funcionario_data)
            except:
                continue
        
        # Ordena por proximidade das férias
        funcionarios_ferias.sort(key=lambda x: x['dias_restantes'])
        
        return render_template('rh.html', 
                            solicitacoes=solicitacoes,
                            funcionarios_ferias=funcionarios_ferias)
    
    except Exception as e:
        return f"Erro ao processar dados: {str(e)}", 500

@app.route('/funcionario')
def painel_funcionario():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        df = pd.read_csv(fr'.\tests\static\csv\FuncionarioBase.csv', sep=';')
        funcionario_id = session.get('funcionario_id', 1)
        funcionario = df[df['ID'] == funcionario_id].to_dict('records')
        
        if not funcionario:
            return "Funcionário não encontrado", 404
        
        return render_template('funcionario.html', 
                            funcionario=funcionario[0],
                            colunas=df.columns.tolist())
    except Exception as e:
        return f"Erro ao ler o arquivo CSV: {str(e)}", 500
    
# Adicione no app.py
@app.route('/solicitacoes')
def solicitacoes():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Exemplo de solicitações existentes (substitua por dados reais)
    solicitacoes_anteriores = [
        {'tipo': 'Férias', 'data': '2023-05-15', 'status': 'Aprovada'},
        {'tipo': 'Banco de Horas', 'data': '2023-06-20', 'status': 'Pendente'}
    ]
    
    return render_template('solicitacoes.html', 
                        funcionario=session.get('username'),
                        solicitacoes=solicitacoes_anteriores)

@app.route('/enviar_solicitacao', methods=['POST'])
def enviar_solicitacao():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Aqui você processaria a solicitação
    tipo = request.form.get('tipo_solicitacao')
    data = request.form.get('data')
    detalhes = request.form.get('detalhes')
    
    # Em um sistema real, você salvaria no banco de dados
    print(f"Nova solicitação de {session['username']}: {tipo} para {data}")
    
    # Redireciona de volta com mensagem de sucesso
    return redirect(url_for('solicitacoes', success=True))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)