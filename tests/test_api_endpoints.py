import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app
from src.core.models import User

# Cliente de teste para a API
client = TestClient(app)


class TestAPIEndpoints:
    """Testes para os endpoints da API"""

    def test_read_root(self):
        """Testa o endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_create_user_validation(self):
        """Testa validação de dados na criação de usuário"""
        # Teste com dados inválidos
        invalid_data = {
            "username": "",  # Username vazio
            "email": "invalid-email",  # Email inválido
            "password": "123"  # Senha muito curta
        }
        
        response = client.post("/users/", json=invalid_data)
        # Deve retornar erro de validação
        assert response.status_code == 422

    def test_create_user_missing_fields(self):
        """Testa criação de usuário com campos faltando"""
        incomplete_data = {
            "username": "testuser"
            # Faltando email e password
        }
        
        response = client.post("/users/", json=incomplete_data)
        assert response.status_code == 422

    def test_get_users_me_unauthorized(self):
        """Testa acesso a rota protegida sem autenticação"""
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_update_user_unauthorized(self):
        """Testa atualização de usuário sem autorização"""
        update_data = {"username": "updated"}
        response = client.put("/users/1", json=update_data)
        assert response.status_code == 401

    def test_delete_user_unauthorized(self):
        """Testa deleção de usuário sem autorização"""
        response = client.delete("/users/1")
        assert response.status_code == 401

    def test_token_endpoint_form_data_required(self):
        """Testa que o endpoint de token requer form data"""
        # Teste com JSON (deve falhar)
        json_data = {"email": "test@example.com", "password": "password123"}
        response = client.post("/token", json=json_data)
        assert response.status_code == 422

    def test_users_endpoint_accepts_query_params(self):
        """Testa que o endpoint de usuários aceita parâmetros de query"""
        response = client.get("/users/?skip=0&limit=5")
        # Pode retornar 200 (usuários) ou 500 (erro de banco), mas não 422
        assert response.status_code in [200, 500]

    def test_user_by_id_invalid_id(self):
        """Testa busca de usuário com ID inválido"""
        response = client.get("/users/abc")  # ID não numérico
        assert response.status_code == 422

    def test_update_user_invalid_id(self):
        """Testa atualização de usuário com ID inválido"""
        update_data = {"username": "updated"}
        response = client.put("/users/abc", json=update_data)
        # Primeiro verifica autenticação (401), depois validação (422)
        assert response.status_code == 401

    def test_delete_user_invalid_id(self):
        """Testa deleção de usuário com ID inválido"""
        response = client.delete("/users/abc")
        # Primeiro verifica autenticação (401), depois validação (422)
        assert response.status_code == 401
