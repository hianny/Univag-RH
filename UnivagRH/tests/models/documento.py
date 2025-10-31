from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Documento(BaseModel):
    __tablename__ = 'documento'

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitacao = Column(Integer, ForeignKey('solicitacao.id_solicitacao'), nullable=False)
    tipo_documento = Column(String(255))
    caminho_documento = Column(String(255))
    tamanho_documento = Column(String(255))

    # Relacionamentos
    solicitacao = relationship("Solicitacao", back_populates="documentos")