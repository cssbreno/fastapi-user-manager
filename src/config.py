import os
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
if SECRET_KEY == "your-super-secret-key":
    logger.warning("⚠️  SECRET_KEY usando valor padrão! Configure SECRET_KEY em produção!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Validações de configuração
if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES deve ser positivo")

# Configurações do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./user_manager.db")

logger.info(f"🔧 Configuração carregada: ALGORITHM={ALGORITHM}, TOKEN_EXPIRE={ACCESS_TOKEN_EXPIRE_MINUTES}min")