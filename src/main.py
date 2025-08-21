from fastapi import FastAPI
from src.infrastructure.web.api import router as api_router
from src.infrastructure.database.database import create_db_and_tables
import logging
from datetime import datetime

# Configurar logger
logger = logging.getLogger(__name__)

# Cria as tabelas no banco de dados na inicialização
try:
    create_db_and_tables()
    logger.info("🚀 Aplicação inicializada com sucesso")
except Exception as e:
    logger.error(f"❌ Erro na inicialização: {e}")
    raise

# Instancia a aplicação FastAPI
app = FastAPI(
    title="API de Gerenciamento de Usuários",
    description="Uma API REST para gerenciar usuários seguindo a Arquitetura Hexagonal.",
    version="1.0.0",
)

# Inclui o roteador da API
app.include_router(api_router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Usuários!"}


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": "connected"
    }
