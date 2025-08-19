import unittest
from unittest.mock import MagicMock

from src.core.models import User
from src.core.ports.user_repository import UserRepository
from src.core.services.user_service import UserService


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

        # Configura o mock para retornar o usuário esperado quando 'add' for chamado
        self.mock_repo.add.return_value = expected_user

        # Chama o método do serviço
        created_user = self.user_service.create_user(user_data)

        # Verifica se o método 'add' do repositório foi chamado com os dados corretos
        self.mock_repo.add.assert_called_once_with(user_data)
        # Verifica se o usuário retornado é o esperado
        self.assertEqual(created_user, expected_user)

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


if __name__ == "__main__":
    unittest.main()
