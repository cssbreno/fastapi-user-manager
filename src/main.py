from fastapi import FastAPI
from src.infrastructure.web.api import router as api_router
from src.infrastructure.database.database import create_db_and_tables

# Cria as tabelas no banco de dados na inicialização
create_db_and_tables()

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
