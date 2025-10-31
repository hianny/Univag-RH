from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class FluxoAprovacao(BaseModel):
    __tablename__ = 'fluxo_aprovacao'

    id_fluxo = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitacao = Column(Integer, ForeignKey('solicitacao.id_solicitacao'))
    id_funcionario = Column(Integer, ForeignKey('funcionarios.id_func'))
    status_solicitacao = Column(String(255))
    data_aprovacao_solicitacao = Column(Date)
    observacao_solicitacao = Column(String(255))

    # Relacionamentos
    solicitacao = relationship("Solicitacao", back_populates="fluxos_aprovacao")
    funcionario = relationship("Funcionarios", back_populates="fluxos_aprovacao")