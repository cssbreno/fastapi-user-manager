from typing import List, Optional
from src.core.ports.user_repository import UserRepository
from src.core.models import User


class UserService:
    """
    Serviço que contém a lógica de negócio para gerenciamento de usuários.
    Ele utiliza a porta UserRepository para interagir com a camada de dados.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict) -> User:
        # Aqui poderiam existir regras de negócio, validações, etc.
        return self.user_repository.add(user_data)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)

    def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return self.user_repository.get_all(skip=skip, limit=limit)

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        return self.user_repository.update(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)
