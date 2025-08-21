from typing import List, Optional
from src.core.ports.user_repository import UserRepository
from src.core.models import User
from src.core.exceptions import UserAlreadyExistsError, UserNotFoundError
import logging

logger = logging.getLogger(__name__)


class UserService:
    """
    Serviço que contém a lógica de negócio para gerenciamento de usuários.
    Ele utiliza a porta UserRepository para interagir com a camada de dados.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict) -> User:
        """Cria um novo usuário com validações de negócio"""
        # Verificar se usuário já existe
        existing_user = self.user_repository.get_by_email(user_data.get("email"))
        if existing_user:
            logger.warning(f"Tentativa de criar usuário com email existente: {user_data.get('email')}")
            raise UserAlreadyExistsError(f"Usuário com email {user_data.get('email')} já existe")
        
        logger.info(f"Criando novo usuário: {user_data.get('email')}")
        return self.user_repository.add(user_data)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            logger.debug(f"Usuário não encontrado com ID: {user_id}")
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        user = self.user_repository.get_by_email(email)
        if not user:
            logger.debug(f"Usuário não encontrado com email: {email}")
        return user

    def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """Lista usuários com paginação"""
        if skip < 0:
            skip = 0
        if limit <= 0 or limit > 100:
            limit = 10
        
        logger.debug(f"Listando usuários: skip={skip}, limit={limit}")
        return self.user_repository.get_all(skip=skip, limit=limit)

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Atualiza usuário existente"""
        # Verificar se usuário existe
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            logger.warning(f"Tentativa de atualizar usuário inexistente: {user_id}")
            raise UserNotFoundError(f"Usuário com ID {user_id} não encontrado")
        
        logger.info(f"Atualizando usuário: {user_id}")
        return self.user_repository.update(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        """Remove usuário"""
        # Verificar se usuário existe
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            logger.warning(f"Tentativa de deletar usuário inexistente: {user_id}")
            raise UserNotFoundError(f"Usuário com ID {user_id} não encontrado")
        
        logger.info(f"Deletando usuário: {user_id}")
        return self.user_repository.delete(user_id)
