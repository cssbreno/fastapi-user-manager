import unittest
from unittest.mock import MagicMock

from src.core.models import User
from src.core.ports.user_repository import UserRepository
from src.core.services.user_service import UserService
from src.core.exceptions import UserNotFoundError


class TestUserService(unittest.TestCase):

    def setUp(self):
        # Cria um mock (dublê) do repositório
        self.mock_repo = MagicMock(spec=UserRepository)
        # Instancia o serviço com o repositório mockado
        self.user_service = UserService(self.mock_repo)

    def test_create_user(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "hashed_password",
        }
        expected_user = User(id=1, **user_data)

        # Configura o mock para retornar None quando verificar se usuário existe
        self.mock_repo.get_by_email.return_value = None
        # Configura o mock para retornar o usuário esperado quando 'add' for chamado
        self.mock_repo.add.return_value = expected_user

        # Chama o método do serviço
        created_user = self.user_service.create_user(user_data)

        # Verifica se o método 'get_by_email' foi chamado para verificar duplicação
        self.mock_repo.get_by_email.assert_called_once_with("test@example.com")
        # Verifica se o método 'add' do repositório foi chamado com os dados corretos
        self.mock_repo.add.assert_called_once_with(user_data)
        # Verifica se o usuário retornado é o esperado
        self.assertEqual(created_user, expected_user)

    def test_create_user_duplicate_email(self):
        """Testa se o serviço rejeita usuários com email duplicado"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "hashed_password",
        }
        
        # Configura o mock para retornar um usuário existente
        existing_user = User(id=1, **user_data)
        self.mock_repo.get_by_email.return_value = existing_user

        # Verifica se a exceção é lançada
        with self.assertRaises(Exception) as context:
            self.user_service.create_user(user_data)
        
        # Verifica se a exceção é do tipo correto
        self.assertIn("já existe", str(context.exception))

    def test_get_user_by_id(self):
        user_id = 1
        expected_user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            hashed_password="fake",
        )

        self.mock_repo.get_by_id.return_value = expected_user

        user = self.user_service.get_user_by_id(user_id)

        self.mock_repo.get_by_id.assert_called_once_with(user_id)
        self.assertEqual(user, expected_user)

    def test_get_user_by_id_not_found(self):
        user_id = 99
        self.mock_repo.get_by_id.return_value = None

        user = self.user_service.get_user_by_id(user_id)

        self.mock_repo.get_by_id.assert_called_once_with(user_id)
        self.assertIsNone(user)

    def test_get_user_by_email(self):
        email = "test@example.com"
        expected_user = User(
            id=1,
            username="testuser",
            email=email,
            hashed_password="fake",
        )

        self.mock_repo.get_by_email.return_value = expected_user

        user = self.user_service.get_user_by_email(email)

        self.mock_repo.get_by_email.assert_called_once_with(email)
        self.assertEqual(user, expected_user)

    def test_get_user_by_email_not_found(self):
        email = "nonexistent@example.com"
        self.mock_repo.get_by_email.return_value = None

        user = self.user_service.get_user_by_email(email)

        self.mock_repo.get_by_email.assert_called_once_with(email)
        self.assertIsNone(user)

    def test_get_all_users(self):
        expected_users = [
            User(
                id=1, username="user1", email="user1@example.com", hashed_password="pw1"
            ),
            User(
                id=2, username="user2", email="user2@example.com", hashed_password="pw2"
            ),
        ]
        self.mock_repo.get_all.return_value = expected_users

        users = self.user_service.get_all_users(skip=0, limit=10)

        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=10)
        self.assertEqual(users, expected_users)

    def test_get_all_users_with_negative_skip(self):
        """Testa se o serviço corrige valores negativos de skip"""
        expected_users = []
        self.mock_repo.get_all.return_value = expected_users

        users = self.user_service.get_all_users(skip=-5, limit=10)

        # Verifica se skip foi corrigido para 0
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=10)
        self.assertEqual(users, expected_users)

    def test_get_all_users_with_invalid_limit(self):
        """Testa se o serviço corrige valores inválidos de limit"""
        expected_users = []
        self.mock_repo.get_all.return_value = expected_users

        # Testa limit muito baixo
        users = self.user_service.get_all_users(skip=0, limit=0)
        self.mock_repo.get_all.assert_called_with(skip=0, limit=10)

        # Testa limit muito alto
        users = self.user_service.get_all_users(skip=0, limit=200)
        self.mock_repo.get_all.assert_called_with(skip=0, limit=10)

    def test_update_user(self):
        user_id = 1
        user_data = {"username": "updated_user"}
        expected_user = User(
            id=user_id,
            username="updated_user",
            email="test@example.com",
            hashed_password="fake",
        )

        # Mock para verificar se usuário existe
        existing_user = User(
            id=user_id,
            username="old_user",
            email="test@example.com",
            hashed_password="fake",
        )
        self.mock_repo.get_by_id.return_value = existing_user
        self.mock_repo.update.return_value = expected_user

        user = self.user_service.update_user(user_id, user_data)

        self.mock_repo.get_by_id.assert_called_once_with(user_id)
        self.mock_repo.update.assert_called_once_with(user_id, user_data)
        self.assertEqual(user, expected_user)

    def test_update_user_not_found(self):
        """Testa se o serviço rejeita atualização de usuário inexistente"""
        user_id = 99
        user_data = {"username": "updated_user"}

        self.mock_repo.get_by_id.return_value = None

        with self.assertRaises(UserNotFoundError) as context:
            self.user_service.update_user(user_id, user_data)

        self.assertIn("não encontrado", str(context.exception))
        self.mock_repo.get_by_id.assert_called_once_with(user_id)
        self.mock_repo.update.assert_not_called()

    def test_delete_user(self):
        user_id = 1
        existing_user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            hashed_password="fake",
        )

        self.mock_repo.get_by_id.return_value = existing_user
        self.mock_repo.delete.return_value = True

        result = self.user_service.delete_user(user_id)

        self.mock_repo.get_by_id.assert_called_once_with(user_id)
        self.mock_repo.delete.assert_called_once_with(user_id)
        self.assertTrue(result)

    def test_delete_user_not_found(self):
        """Testa se o serviço rejeita deleção de usuário inexistente"""
        user_id = 99

        self.mock_repo.get_by_id.return_value = None

        with self.assertRaises(UserNotFoundError) as context:
            self.user_service.delete_user(user_id)

        self.assertIn("não encontrado", str(context.exception))
        self.mock_repo.get_by_id.assert_called_once_with(user_id)
        self.mock_repo.delete.assert_not_called()


if __name__ == "__main__":
    unittest.main()
