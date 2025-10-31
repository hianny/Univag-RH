from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from .base import BaseModel

class Solicitacao(BaseModel):
    __tablename__ = 'solicitacao'

    id_solicitacao = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('usuario.id_user'), nullable=False)
    id_tipo_solicitacao = Column(Integer, ForeignKey('tipo_solicitacao.id_tipo_solicitacao'), nullable=False)
    mensagem_solicitacao = Column(String(255))
    data_solicitacao = Column(Date, nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="solicitacoes")
    tipo_solicitacao = relationship("TipoSolicitacao", back_populates="solicitacoes")
    fluxos_aprovacao = relationship("FluxoAprovacao", back_populates="solicitacao")
    documentos = relationship("Documento", back_populates="solicitacao")
