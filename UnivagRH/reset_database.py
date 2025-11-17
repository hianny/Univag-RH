from werkzeug.security import generate_password_hash
from tests.ext.database import db
from tests.app import create_app
from tests.models import Usuario, Funcionarios, UsuariosDetalhes, TipoSolicitacao

def recriar_banco():

    app = create_app()

    with app.app_context():

        db.drop_all()
        db.create_all()

        # Criar tipos de solicitação
        tipos = [
            TipoSolicitacao(nome_tipo_solicitacao='Ferias', descricao_tipo_solicitacao='Férias'),
            TipoSolicitacao(nome_tipo_solicitacao='Atestado', descricao_tipo_solicitacao='Atestado Médico'),
            TipoSolicitacao(nome_tipo_solicitacao='Declaracao', descricao_tipo_solicitacao='Declaração de Vínculo'),
            TipoSolicitacao(nome_tipo_solicitacao='Holerite', descricao_tipo_solicitacao='Segunda Via de Holerite'),
            TipoSolicitacao(nome_tipo_solicitacao='Progressao', descricao_tipo_solicitacao='Consulta de Progressão Salarial'),
            TipoSolicitacao(nome_tipo_solicitacao='Outros', descricao_tipo_solicitacao='Outros'),
        ]

        for tipo in tipos:
            if not TipoSolicitacao.query.filter_by(nome_tipo_solicitacao=tipo.nome_tipo_solicitacao).first():
                db.session.add(tipo)

        # Dados dos usuários (similar ao dicionário original)
        usuarios_data = [
            {'login': 'rh', 'senha': 'rh123', 'rh': True},
            {'login': 'hianny', 'senha': '123', 'rh': False, 'nome': 'Hianny', 'cpf': '06911628164', 'email': 'hiannymaria@gmail.com', 'cargo': 'Programadora', 'salario': '1000', 'endereco': 'rua jandaia estrela'},
            {'login': 'joao', 'senha': '123', 'rh': False, 'nome': 'João', 'cpf': '09016378165', 'email': 'fabio@gmail.com', 'cargo': 'Professor', 'salario': '5000', 'endereco': 'rua jandaia cubo'},
            {'login': 'maria', 'senha': '123', 'rh': False, 'nome': 'Maria', 'cpf': '26529860977', 'email': 'joana@gmail.com', 'cargo': 'Jornalista', 'salario': '2500', 'endereco': 'rua jandaia triangulo'}
        ]

        for i, user_data in enumerate(usuarios_data, 1):
            if not Usuario.query.filter_by(login_user=user_data['login']).first():
                usuario = Usuario(
                    login_user=user_data['login'],
                    senha_user= generate_password_hash(user_data['senha']),
                    rh=user_data['rh']
                )
                db.session.add(usuario)
                db.session.flush()  # Para obter o id

                if not user_data['rh']:
                    # Criar funcionário
                    funcionario = Funcionarios(
                        nome_func=user_data['nome'],
                        cpf_func=user_data['cpf'],
                        id_user=usuario.id_user
                    )
                    db.session.add(funcionario)

                    # Criar detalhes
                    detalhes = UsuariosDetalhes(
                        id_user=usuario.id_user,
                        nome=user_data['nome'],
                        cpf=user_data['cpf'],
                        email=user_data['email'],
                        cargo=user_data['cargo'],
                        salario=user_data['salario'],
                        endereco=user_data['endereco'],
                    )
                    db.session.add(detalhes)

        db.session.commit()
        print("✅ Dados iniciais criados com sucesso!")

if __name__ == '__main__':
    recriar_banco()