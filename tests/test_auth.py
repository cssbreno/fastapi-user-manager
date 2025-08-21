import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from src.infrastructure.web.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user
)
from src.infrastructure.web import schemas
from src.core.models import User as UserDomain


class TestAuth(unittest.TestCase):

    def test_verify_password_correct(self):
        """Testa verificação de senha correta"""
        password = "testpassword"
        hashed_password = get_password_hash(password)
        
        result = verify_password(password, hashed_password)
        self.assertTrue(result)

    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta"""
        password = "testpassword"
        wrong_password = "wrongpassword"
        hashed_password = get_password_hash(password)
        
        result = verify_password(wrong_password, hashed_password)
        self.assertFalse(result)

    def test_get_password_hash(self):
        """Testa geração de hash de senha"""
        password = "testpassword"
        
        hashed = get_password_hash(password)
        
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        self.assertTrue(len(hashed) > len(password))

    def test_create_access_token_default_expiry(self):
        """Testa criação de token com expiração padrão"""
        data = {"sub": "test@example.com"}
        
        token = create_access_token(data)
        
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

    def test_create_access_token_custom_expiry(self):
        """Testa criação de token com expiração customizada"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=60)
        
        token = create_access_token(data, expires_delta)
        
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

    @patch('src.infrastructure.web.auth.jwt.decode')
    @patch('src.infrastructure.web.auth.SQLiteUserRepository')
    @patch('src.infrastructure.web.auth.UserService')
    def test_get_current_active_user_valid_token(self, mock_user_service, mock_repo, mock_jwt_decode):
        """Testa obtenção de usuário ativo com token válido"""
        # Mock do token JWT
        mock_jwt_decode.return_value = {
            "sub": "test@example.com",
            "exp": datetime.now(timezone.utc).timestamp() + 3600
        }
        
        # Mock do usuário
        mock_user = UserDomain(
            id=1,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        # Mock do serviço
        mock_service_instance = MagicMock()
        mock_service_instance.get_user_by_email.return_value = mock_user
        mock_user_service.return_value = mock_service_instance
        
        # Mock da sessão
        mock_session = MagicMock()
        
        # Mock do token
        mock_token = "valid_token"
        
        # Mock do oauth2_scheme
        with patch('src.infrastructure.web.auth.oauth2_scheme', return_value=mock_token):
            result = get_current_active_user(mock_token, mock_session)
        
        self.assertIsInstance(result, schemas.UserResponse)
        self.assertEqual(result.email, "test@example.com")

    @patch('src.infrastructure.web.auth.jwt.decode')
    def test_get_current_active_user_invalid_token_no_sub(self, mock_jwt_decode):
        """Testa token inválido sem sub claim"""
        mock_jwt_decode.return_value = {"exp": datetime.now(timezone.utc).timestamp() + 3600}
        
        mock_session = MagicMock()
        mock_token = "invalid_token"
        
        with patch('src.infrastructure.web.auth.oauth2_scheme', return_value=mock_token):
            with self.assertRaises(HTTPException) as context:
                get_current_active_user(mock_token, mock_session)
            
            self.assertEqual(context.exception.status_code, 401)

    @patch('src.infrastructure.web.auth.jwt.decode')
    def test_get_current_active_user_expired_token(self, mock_jwt_decode):
        """Testa token expirado"""
        mock_jwt_decode.return_value = {
            "sub": "test@example.com",
            "exp": datetime.now(timezone.utc).timestamp() - 3600  # Token expirado
        }
        
        mock_session = MagicMock()
        mock_token = "expired_token"
        
        with patch('src.infrastructure.web.auth.oauth2_scheme', return_value=mock_token):
            with self.assertRaises(HTTPException) as context:
                get_current_active_user(mock_token, mock_session)
            
            self.assertEqual(context.exception.status_code, 401)

    @patch('src.infrastructure.web.auth.jwt.decode')
    @patch('src.infrastructure.web.auth.SQLiteUserRepository')
    @patch('src.infrastructure.web.auth.UserService')
    def test_get_current_active_user_user_not_found(self, mock_user_service, mock_repo, mock_jwt_decode):
        """Testa usuário não encontrado para token válido"""
        # Mock do token JWT válido
        mock_jwt_decode.return_value = {
            "sub": "test@example.com",
            "exp": datetime.now(timezone.utc).timestamp() + 3600
        }
        
        # Mock do serviço retornando None
        mock_service_instance = MagicMock()
        mock_service_instance.get_user_by_email.return_value = None
        mock_user_service.return_value = mock_service_instance
        
        mock_session = MagicMock()
        mock_token = "valid_token"
        
        with patch('src.infrastructure.web.auth.oauth2_scheme', return_value=mock_token):
            with self.assertRaises(HTTPException) as context:
                get_current_active_user(mock_token, mock_session)
            
            self.assertEqual(context.exception.status_code, 401)

    @patch('src.infrastructure.web.auth.jwt.decode')
    def test_get_current_active_user_jwt_error(self, mock_jwt_decode):
        """Testa erro na decodificação do JWT"""
        from jose import JWTError
        mock_jwt_decode.side_effect = JWTError("JWT decode error")
        
        mock_session = MagicMock()
        mock_token = "invalid_token"
        
        with patch('src.infrastructure.web.auth.oauth2_scheme', return_value=mock_token):
            with self.assertRaises(HTTPException) as context:
                get_current_active_user(mock_token, mock_session)
            
            self.assertEqual(context.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()
