from sqlalchemy.orm import Session
from src.infrastructure.database.database import SessionLocal


def get_db():
    """
    Dependência do FastAPI para fornecer uma sessão de banco de dados por requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
