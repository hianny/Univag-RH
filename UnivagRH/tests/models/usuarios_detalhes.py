from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class UsuariosDetalhes(BaseModel):
    __tablename__ = 'usuarios_detalhes'

    id_usuario_detalhe = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('usuario.id_user'), nullable=False)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    endereco = Column(String(255))
    data_nascimento = Column(Date)
    cargo = Column(String(100))
    salario = Column(DECIMAL(10, 2))

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="detalhes")