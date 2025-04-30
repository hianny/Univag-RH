from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Adicione mais usuários conforme necessário
USUARIOS = {
    'rh': {'senha': 'rh123', 'tipo': 'rh'},
    'func': {'senha': 'func123', 'tipo': 'funcionario'},
    'joao': {'senha': '123', 'tipo': 'funcionario', 'id': 1},
    'maria': {'senha': '123', 'tipo': 'funcionario', 'id': 2}
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
        df = pd.read_csv(fr'.\tests\static\csv\FuncionarioBase.csv', sep=';')
        
        # Filtro por nome
        nome_filtro = request.args.get('nome', '').lower()
        if nome_filtro:
            df = df[df['Nome'].str.lower().str.contains(nome_filtro)]
        
        colunas = df.columns.tolist()
        dados = df.to_dict('records')
        
        return render_template('rh.html', 
                            funcionarios=dados, 
                            colunas=colunas,
                            nome_filtro=nome_filtro)
    except Exception as e:
        return f"Erro ao ler o arquivo CSV: {str(e)}", 500

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)