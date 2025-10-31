from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from flask_login import current_user, login_user

from tests.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

# # Adicione mais usuários conforme necessário
# USUARIOS = {
#     'rh': {'senha': 'rh123', 'tipo': 'rh'},
#     'hianny': {'senha': '1w23', 'tipo': 'funcionario', 'id': 1},
#     'joao': {'senha': '123', 'tipo': 'funcionario', 'id': 2},
#     'maria': {'senha': '123', 'tipo': 'funcionario', 'id': 3}
# }



@auth_bp.route('/')
def index():
    print(current_user.is_authenticated)
    print(current_user.get_id())
    if current_user.is_authenticated:
        if current_user.rh:
            return redirect(url_for('rh.painel'))
        else:
            return redirect(url_for('funcionario.painel'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        usuario = AuthService.autenticar(username, password)

        if usuario:
            login_user(usuario)

            if usuario.rh:
                return redirect(url_for('rh.painel'))
            else:
                return redirect(url_for('funcionario.painel'))
        else:
            flash('Usuário ou senha inválidos.', 'error')

        # if username in USUARIOS and USUARIOS[username]['senha'] == password:
        #     session['username'] = username
        #     session['tipo_usuario'] = USUARIOS[username]['tipo']
        #
        #     if USUARIOS[username]['tipo'] == 'funcionario':
        #         session['funcionario_id'] = USUARIOS[username].get('id', 1)
        #
        #         # Carrega os dados do funcionário do CSV e armazena na sessão
        #         try:
        #             df_funcionarios = pd.read_csv(r'./UnivagRH/tests/static/csv/FuncionarioBase.csv', sep=';')
        #             funcionario_data = df_funcionarios[df_funcionarios['ID'] == session['funcionario_id']].to_dict(
        #                 'records')
        #             if funcionario_data:
        #                 session['funcionario_data'] = funcionario_data[0]
        #             else:
        #                 session['funcionario_data'] = {}  # Caso o ID não seja encontrado
        #         except Exception as e:
        #             print(f"Erro ao carregar dados do funcionário do CSV: {e}")
        #             session['funcionario_data'] = {}
        #
        #         # Inicializa a lista de solicitações do funcionário na sessão (se não existir)
        #         if 'solicitacoes_funcionario_data' not in session:
        #             session['solicitacoes_funcionario_data'] = [
        #                 # Exemplo de dados iniciais, em um app real viriam de um DB
        #                 {'tipo': 'Férias', 'data': '2024-03-01', 'status': 'Aprovado',
        #                  'observacao': 'Férias aprovadas para Março.'},
        #                 {'tipo': 'Atestado', 'data': '2024-04-10', 'status': 'Pendente',
        #                  'observacao': 'Aguardando validação do RH.'},
        #                 {'tipo': 'Declaração', 'data': '2024-02-20', 'status': 'Rejeitado',
        #                  'observacao': 'Documentação incompleta.'}
        #             ]
        #
        #     if USUARIOS[username]['tipo'] == 'rh':
        #         return redirect(url_for('rh.painel'))
        #     else:
        #         return redirect(url_for('funcionario.painel'))
        # else:
        #     return render_template('login.html', erro="Usuário ou senha inválidos")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    return redirect(url_for('auth.login'))
