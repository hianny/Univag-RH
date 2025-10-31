from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import BaseModel

class TipoSolicitacao(BaseModel):
    __tablename__ = 'tipo_solicitacao'

    id_tipo_solicitacao = Column(Integer, primary_key=True, autoincrement=True)
    nome_tipo_solicitacao = Column(String(100), nullable=False)
    descricao_tipo_solicitacao = Column(String(255))

    # Relacionamentos
    solicitacoes = relationship("Solicitacao", back_populates="tipo_solicitacao")