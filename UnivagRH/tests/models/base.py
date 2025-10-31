from tests.ext.database import db


class BaseModel(db.Model):
    """Classe base com métodos comuns para todos os modelos"""
    __abstract__ = True

    # Campos comuns (opcional)
    # created_at = Column(DateTime, default=datetime.now(UTC))
    # updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    # MÉTODOS COMUNS DE CRUD
    def save(self):
        """Salva o objeto no banco"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Remove o objeto do banco"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Atualiza campos do objeto"""
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        db.session.commit()
        return self

    # MÉTODOS DE CONSULTA (CLASS METHODS)
    @classmethod
    def get_by_id(cls, id: int):
        """Busca por ID"""
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        """Busca todos"""
        return cls.query.all()

    @classmethod
    def find_first_by(cls, **filters):
        """Busca primeiro resultado por filtros"""
        return cls.query.filter_by(**filters).first()

    @classmethod
    def find_all_by(cls, **filters):
        """Busca todos por filtros"""
        return cls.query.filter_by(**filters).all()

    @classmethod
    def create(cls, **kwargs):
        """Cria e salva novo objeto"""
        instance = cls(**kwargs)
        return instance.save()

    # SERIALIZAÇÃO
    def to_dict(self):
        """Converte objeto para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }