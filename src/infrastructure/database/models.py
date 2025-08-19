from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    """
    Modelo SQLAlchemy que representa a tabela de usuários no banco de dados.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
