from typing import List, Optional
from sqlalchemy.orm import Session

from src.core.ports.user_repository import UserRepository
from src.core.models import User as UserDomain
from src.infrastructure.database.models import User as UserModelDB


class SQLiteUserRepository(UserRepository):
    """
    Implementação concreta (Adapter) do UserRepository para SQLite usando SQLAlchemy.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, user_data: dict) -> UserDomain:
        db_user = UserModelDB(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserDomain.model_validate(db_user)

    def get_by_id(self, user_id: int) -> Optional[UserDomain]:
        db_user = self.db.query(UserModelDB).filter(UserModelDB.id == user_id).first()
        if db_user:
            return UserDomain.model_validate(db_user)
        return None

    def get_by_email(self, email: str) -> Optional[UserDomain]:
        db_user = self.db.query(UserModelDB).filter(UserModelDB.email == email).first()
        if db_user:
            return UserDomain.model_validate(db_user)
        return None

    def get_all(self, skip: int = 0, limit: int = 10) -> List[UserDomain]:
        users_db = self.db.query(UserModelDB).offset(skip).limit(limit).all()
        return [UserDomain.model_validate(user) for user in users_db]

    def update(self, user_id: int, user_data: dict) -> Optional[UserDomain]:
        db_user = self.db.query(UserModelDB).filter(UserModelDB.id == user_id).first()
        if db_user:
            for key, value in user_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
            return UserDomain.model_validate(db_user)
        return None

    def delete(self, user_id: int) -> bool:
        db_user = self.db.query(UserModelDB).filter(UserModelDB.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
