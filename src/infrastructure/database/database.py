from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

# ✅ SOLUÇÃO: Import moderno para SQLAlchemy 2.0
Base = declarative_base()

# Configuração do engine com logging
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False  # Set to True para debug SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Cria as tabelas no banco de dados"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas do banco de dados criadas com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        raise
