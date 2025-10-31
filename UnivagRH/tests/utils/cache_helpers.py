from functools import lru_cache

from tests.models import TipoSolicitacao
from tests.services.solicitacao_service import SolicitacaoService


class TipoSolicitacaoCache:
    @staticmethod
    @lru_cache(maxsize=1)
    def get_all():
        return SolicitacaoService.get_tipos_solicitacao()

    @staticmethod
    def get_by_id(tipo_id):
        tipos = TipoSolicitacaoCache.get_all()
        return next((t for t in tipos if t['id'] == int(tipo_id)), None)

    @staticmethod
    def invalidate():
        TipoSolicitacaoCache.get_all.cache_clear()