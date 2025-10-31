from datetime import datetime, UTC

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Boolean, String, Integer, desc
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel

class Usuario(UserMixin, BaseModel):
    __tablename__ = 'usuario'

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    login_user = Column(String(100), nullable=False, unique=True)
    senha_user = Column(String(255), nullable=False)
    ativo_user = Column(Boolean, nullable=False, default=True)
    rh = Column(Boolean, nullable=False, default=False)
    data_criacao_user = Column(DateTime, nullable=False, default=datetime.now(UTC))

    # Relacionamentos
    funcionario = relationship("Funcionarios", back_populates="usuario", uselist=False)
    solicitacoes = relationship("Solicitacao", back_populates="usuario")
    detalhes = relationship("UsuariosDetalhes", back_populates="usuario", uselist=False)

    def set_password(self, password: str):
        self.senha_user = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica se a senha está correta"""
        try:
            return check_password_hash(self.senha_user, password)
        except:
            return self.senha_user == password  # Fallback

    def get_id(self):
        return self.id_user

    @classmethod
    def get_by_login(cls, login):
        return cls.find_first_by(login_user=login)

    def change_password(self, new_password):
        self.senha_user = new_password
        return self.save()
