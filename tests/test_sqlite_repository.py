import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.infrastructure.database.sqlite_user_repository import SQLiteUserRepository
from src.infrastructure.database.models import User as UserModel
from src.core.models import User as UserDomain


class TestSQLiteUserRepository(unittest.TestCase):

    def setUp(self):
        # Mock da sessão do banco de dados
        self.mock_session = MagicMock(spec=Session)
        self.repository = SQLiteUserRepository(self.mock_session)

    def test_add_user(self):
        """Testa adição de usuário"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "hashed_password"
        }
        
        # Mock do usuário criado
        mock_user = UserModel(
            id=1,
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=user_data["hashed_password"]
        )
        
        # Configurar o mock para retornar o usuário
        self.mock_session.add.return_value = None
        self.mock_session.commit.return_value = None
        self.mock_session.refresh.return_value = None
        
        # Mock do query para retornar o usuário após refresh
        mock_query = MagicMock()
        mock_query.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query
        
        # Mock do refresh para definir o ID
        def mock_refresh(user):
            user.id = 1
        
        self.mock_session.refresh.side_effect = mock_refresh

        result = self.repository.add(user_data)

        # Verificar se os métodos foram chamados
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once()
        
        # Verificar se o resultado é do tipo correto
        self.assertIsInstance(result, UserDomain)
        self.assertEqual(result.username, user_data["username"])
        self.assertEqual(result.email, user_data["email"])

    def test_get_by_id_found(self):
        """Testa busca de usuário por ID - encontrado"""
        user_id = 1
        mock_user = UserModel(
            id=user_id,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        # Mock do query
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_id(user_id)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.assertIsInstance(result, UserDomain)
        self.assertEqual(result.id, user_id)

    def test_get_by_id_not_found(self):
        """Testa busca de usuário por ID - não encontrado"""
        user_id = 99
        
        # Mock do query retornando None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_id(user_id)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.assertIsNone(result)

    def test_get_by_email_found(self):
        """Testa busca de usuário por email - encontrado"""
        email = "test@example.com"
        mock_user = UserModel(
            id=1,
            username="testuser",
            email=email,
            hashed_password="hashed_password"
        )
        
        # Mock do query
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_email(email)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.assertIsInstance(result, UserDomain)
        self.assertEqual(result.email, email)

    def test_get_by_email_not_found(self):
        """Testa busca de usuário por email - não encontrado"""
        email = "nonexistent@example.com"
        
        # Mock do query retornando None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_email(email)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.assertIsNone(result)

    def test_get_all_users(self):
        """Testa listagem de usuários com paginação"""
        mock_users = [
            UserModel(id=1, username="user1", email="user1@example.com", hashed_password="pw1"),
            UserModel(id=2, username="user2", email="user2@example.com", hashed_password="pw2"),
        ]
        
        # Mock do query
        mock_query = MagicMock()
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = mock_users
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_all(skip=0, limit=10)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], UserDomain)
        self.assertIsInstance(result[1], UserDomain)

    def test_update_user_found(self):
        """Testa atualização de usuário - encontrado"""
        user_id = 1
        user_data = {"username": "updated_user"}
        
        mock_user = UserModel(
            id=user_id,
            username="old_user",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        # Mock do query
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query
        
        # Mock do commit
        self.mock_session.commit.return_value = None

        result = self.repository.update(user_id, user_data)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.mock_session.commit.assert_called_once()
        self.assertIsInstance(result, UserDomain)
        self.assertEqual(result.username, "updated_user")

    def test_update_user_not_found(self):
        """Testa atualização de usuário - não encontrado"""
        user_id = 99
        user_data = {"username": "updated_user"}
        
        # Mock do query retornando None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        self.mock_session.query.return_value = mock_query

        result = self.repository.update(user_id, user_data)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.assertIsNone(result)

    def test_delete_user_found(self):
        """Testa deleção de usuário - encontrado"""
        user_id = 1
        mock_user = UserModel(
            id=user_id,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        # Mock do query
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query
        
        # Mock do delete e commit
        self.mock_session.delete.return_value = None
        self.mock_session.commit.return_value = None

        result = self.repository.delete(user_id)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.mock_session.delete.assert_called_once_with(mock_user)
        self.mock_session.commit.assert_called_once()
        self.assertTrue(result)

    def test_delete_user_not_found(self):
        """Testa deleção de usuário - não encontrado"""
        user_id = 99
        
        # Mock do query retornando None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        self.mock_session.query.return_value = mock_query

        result = self.repository.delete(user_id)

        self.mock_session.query.assert_called_once_with(UserModel)
        self.mock_session.delete.assert_not_called()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
