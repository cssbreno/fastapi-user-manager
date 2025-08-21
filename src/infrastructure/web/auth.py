from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.infrastructure.web import schemas
from src.infrastructure.web.dependencies import get_db
from src.core.services.user_service import UserService
from src.core.exceptions import InvalidCredentialsError
from src.infrastructure.database.sqlite_user_repository import SQLiteUserRepository
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import logging

logger = logging.getLogger(__name__)

# --- Contexto para Hashing de Senhas ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Esquema de Autenticação ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# --- Funções Auxiliares de Autenticação ---
def verify_password(plain_password, hashed_password):
    """Verifica se a senha em texto plano corresponde ao hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Gera hash da senha usando bcrypt"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT de acesso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Token JWT criado para usuário: {data.get('sub')}")
    return encoded_jwt


def get_current_active_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> schemas.UserResponse:
    """Valida o token JWT e retorna o usuário ativo"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Token JWT inválido: sub claim ausente")
            raise credentials_exception
        
        # Verificar se o token expirou
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            logger.warning(f"Token JWT expirado para usuário: {email}")
            raise credentials_exception
            
        token_data = schemas.TokenData(email=email)
    except JWTError as e:
        logger.warning(f"Erro ao decodificar token JWT: {e}")
        raise credentials_exception

    repository = SQLiteUserRepository(db)
    service = UserService(repository)
    user = service.get_user_by_email(email=token_data.email)

    if user is None:
        logger.warning(f"Usuário não encontrado para token válido: {email}")
        raise credentials_exception
    
    logger.debug(f"Usuário autenticado: {email}")
    return schemas.UserResponse.model_validate(user)
