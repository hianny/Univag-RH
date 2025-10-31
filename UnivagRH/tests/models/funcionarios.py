from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Funcionarios(BaseModel):
    __tablename__ = 'funcionarios'

    id_func = Column(Integer, primary_key=True, autoincrement=True)
    nome_func = Column(String(100), nullable=False)
    cpf_func = Column(String(11), nullable=False, unique=True)
    id_user = Column(Integer, ForeignKey('usuario.id_user'), nullable=False, unique=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="funcionario")
    fluxos_aprovacao = relationship("FluxoAprovacao", back_populates="funcionario")