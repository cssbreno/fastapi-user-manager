from fastapi import APIRouter, Depends, HTTPException, status, Query, Form
from pydantic import EmailStr  # Boa prática para validar o email recebido
from sqlalchemy.orm import Session
from typing import List

from src.core.services.user_service import UserService
from src.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.infrastructure.database.sqlite_user_repository import SQLiteUserRepository
from src.infrastructure.web import schemas
from src.infrastructure.web.dependencies import get_db
from src.infrastructure.web.auth import (
    create_access_token,
    get_current_active_user,
    verify_password,
    get_password_hash,
)
import logging

logger = logging.getLogger(__name__)

# Criação do roteador da API
router = APIRouter()


# --- Helper para instanciar o serviço com suas dependências ---
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = SQLiteUserRepository(db)
    return UserService(repository)


# --- Rotas de Autenticação ---
@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(
    # Substituímos o Depends() por parâmetros de formulário explícitos
    email: EmailStr = Form(..., description="O e-mail do usuário para login."),
    password: str = Form(..., description="A senha do usuário."),
    service: UserService = Depends(get_user_service),
):
    """
    Autentica o usuário e retorna um token de acesso.

    Use o seu **e-mail** e **senha** para obter o token JWT.
    """
    # Agora usamos a variável 'email' diretamente
    user = service.get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Tentativa de login falhou para email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"Login bem-sucedido para email: {email}")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- Rotas de Usuários (CRUD) ---
@router.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user(
    user: schemas.UserCreate, service: UserService = Depends(get_user_service)
):
    try:
        user_data = user.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        return service.create_user(user_data)
    except UserAlreadyExistsError as e:
        logger.warning(f"Tentativa de criar usuário duplicado: {user.email}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/", response_model=List[schemas.UserResponse], tags=["Users"])
def read_users(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Número máximo de registros a retornar"
    ),
    service: UserService = Depends(get_user_service),
):
    """
    Recupera uma lista paginada de usuários.
    """
    users = service.get_all_users(skip=skip, limit=limit)
    logger.debug(f"Listando usuários: {len(users)} encontrados")
    return users


@router.get("/users/me", response_model=schemas.UserResponse, tags=["Users"])
def read_users_me(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
):
    """
    Rota protegida para obter os dados do usuário atualmente logado.
    """
    return current_user


@router.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        db_user = service.get_user_by_id(user_id)
        if db_user is None:
            raise UserNotFoundError(f"Usuário com ID {user_id} não encontrado")
        return db_user
    except UserNotFoundError as e:
        logger.warning(f"Tentativa de acessar usuário inexistente: {user_id}")
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: schemas.UserResponse = Depends(get_current_active_user),
):
    if current_user.id != user_id:
        logger.warning(f"Usuário {current_user.id} tentou atualizar usuário {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    user_data = user_update.model_dump(exclude_unset=True)
    if not user_data:
        raise HTTPException(status_code=400, detail="No data to update")

    try:
        updated_user = service.update_user(user_id, user_data)
        return updated_user
    except UserNotFoundError as e:
        logger.warning(f"Tentativa de atualizar usuário inexistente: {user_id}")
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"]
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: schemas.UserResponse = Depends(get_current_active_user),
):
    if current_user.id != user_id:
        logger.warning(f"Usuário {current_user.id} tentou deletar usuário {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    try:
        if not service.delete_user(user_id):
            raise UserNotFoundError(f"Usuário com ID {user_id} não encontrado")
        logger.info(f"Usuário {user_id} deletado com sucesso")
        return None
    except UserNotFoundError as e:
        logger.warning(f"Tentativa de deletar usuário inexistente: {user_id}")
        raise HTTPException(status_code=404, detail=str(e))
