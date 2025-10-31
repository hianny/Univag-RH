from tests.ext.database import db
from tests.models import TipoSolicitacao, Usuario, Solicitacao, FluxoAprovacao


class SolicitacaoService():

    @staticmethod
    def get_all():
        solicitacoes = Solicitacao.query.all()
        return [{'funcionario': solicitacao.usuario.funcionario.nome_func,
                 'tipo': solicitacao.tipo_solicitacao.descricao_tipo_solicitacao,
                 'data': solicitacao.data_solicitacao.strftime('%d/%m/%Y'),
                 'status': 'Pendente'} for solicitacao in solicitacoes]

    @staticmethod
    def solicitar(id_user: int, id_func: int, id_tipo: int, data: str, mensagem: str) -> bool:
        try:

            user = Usuario.get_by_id(id_user)
            if not user or not user.funcionario:
                raise ValueError("Usuário ou funcionário não encontrado")

            solicitacao = Solicitacao(id_user=id_user, id_tipo_solicitacao=id_tipo, mensagem_solicitacao=mensagem,
                                      data_solicitacao=data)
            db.session.add(solicitacao)
            db.session.flush()

            fluxo_aprovacao = FluxoAprovacao(id_solicitacao=solicitacao.id_solicitacao,
                                             id_funcionario=id_func, status_solicitacao='Pendente',
                                             observacao_solicitacao='Sua solicitação foi recebida e está aguardando análise do RH.')
            db.session.add(fluxo_aprovacao)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # Log do erro
            print(f"Erro ao salvar solicitação: {e}")
            return False

    @staticmethod
    def get_tipos_solicitacao():
        tipos_solicitacao = TipoSolicitacao.get_all()
        return [{'id': tipo.id_tipo_solicitacao, 'descricao': tipo.descricao_tipo_solicitacao} for tipo in
                tipos_solicitacao]

    @staticmethod
    def get_descricao_tipo(id_tipo_solicitacao: int) -> str:
        tipo_solicitacao = TipoSolicitacao.query.get(id_tipo_solicitacao)
        return tipo_solicitacao.escricao_tipo_solicitacao
