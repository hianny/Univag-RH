# services/auth_service.py
from flask_login import login_user

from tests.models import Usuario, UsuariosDetalhes

class AuthService:
    """Service responsável por toda lógica de autenticação"""

    @staticmethod
    def autenticar(login: str, password: str) -> Usuario:
        usuario = Usuario.get_by_login(login)
        if not usuario or not usuario.check_password(password) or not usuario.ativo_user:
            return None
        return usuario

    @staticmethod
    def _montar_dados_sessao(usuario: Usuario) -> dict:
        """Monta dados completos para a sessão"""
        dados_base = {
            'user_id': usuario.id_user,
            'username': usuario.login_user,
            'rh': usuario.rh,
            'is_authenticated': True
        }

        if not usuario.rh:
            dados_base.update(AuthService._carregar_dados_funcionario(usuario))

        return dados_base

    @staticmethod
    def _carregar_dados_funcionario(usuario: Usuario) -> dict:
        """Carrega dados específicos do funcionário"""
        dados = {}

        # ✅ Service coordena múltiplos models
        if usuario.funcionario:
            dados['funcionario_id'] = usuario.funcionario.id_func

        if usuario.detalhes:
            dados['funcionario_data'] = AuthService._formatar_detalhes(usuario.detalhes)

        return dados

    @staticmethod
    def _formatar_detalhes(detalhes: UsuariosDetalhes) -> dict:
        """Formata dados detalhados do usuário"""
        return {
            'ID': detalhes.id_usuario_detalhe,
            'NOME_COMPLETO': detalhes.nome,
            'CARGO': detalhes.cargo,
            'EMAIL': detalhes.email,
            'ENDERECO': detalhes.endereco,
            'SALARIO': detalhes.salario,
            'CPF': detalhes.cpf
        }

    @staticmethod
    def alterar_senha(usuario_id: int, senha_atual: str, nova_senha: str) -> bool:
        """Altera senha do usuário com validação"""
        usuario = Usuario.query.get(usuario_id)

        if not usuario or not usuario.verificar_senha(senha_atual):
            return False

        usuario.definir_senha(nova_senha)
        return True

    # @staticmethod
    # def obter_solicitacoes_usuario(usuario_id: int) -> list:
    #     """Obtém solicitações formatadas do usuário"""
    #
    #     usuario = Usuario.query.get(usuario_id)
    #     if not usuario:
    #         return []
    #
    #     # ✅ Service formata dados de múltiplas fontes
    #     return [{
    #         'tipo': s.tipo_solicitacao.nome_tipo_solicitacao,
    #         'data': s.data_solicitacao.strftime('%Y-%m-%d'),
    #         'status': s.status
    #     } for s in usuario.solicitacoes]