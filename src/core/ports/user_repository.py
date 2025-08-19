from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.models import User


class UserRepository(ABC):
    """
    Interface (Porta) que define as operações de persistência
    para a entidade User. A lógica de negócio depende desta abstração.
    """

    @abstractmethod
    def add(self, user_data: dict) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass

    @abstractmethod
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass
