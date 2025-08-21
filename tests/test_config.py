import unittest
from unittest.mock import patch, MagicMock
import os

from src.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    DATABASE_URL
)


class TestConfig(unittest.TestCase):

    def test_default_values(self):
        """Testa se os valores padrão estão corretos"""
        self.assertEqual(ALGORITHM, "HS256")
        self.assertEqual(ACCESS_TOKEN_EXPIRE_MINUTES, 30)
        self.assertIn("user_manager.db", DATABASE_URL)

    @patch.dict(os.environ, {'SECRET_KEY': 'test-secret-key'})
    def test_secret_key_from_env(self):
        """Testa se SECRET_KEY é carregada do ambiente"""
        # Recarrega o módulo para pegar a nova variável de ambiente
        import importlib
        import src.config
        importlib.reload(src.config)
        
        self.assertEqual(src.config.SECRET_KEY, 'test-secret-key')

    @patch.dict(os.environ, {'ACCESS_TOKEN_EXPIRE_MINUTES': '60'})
    def test_token_expire_from_env(self):
        """Testa se ACCESS_TOKEN_EXPIRE_MINUTES é carregado do ambiente"""
        # Recarrega o módulo para pegar a nova variável de ambiente
        import importlib
        import src.config
        importlib.reload(src.config)
        
        self.assertEqual(src.config.ACCESS_TOKEN_EXPIRE_MINUTES, 60)

    @patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'})
    def test_database_url_from_env(self):
        """Testa se DATABASE_URL é carregado do ambiente"""
        # Recarrega o módulo para pegar a nova variável de ambiente
        import importlib
        import src.config
        importlib.reload(src.config)
        
        self.assertEqual(src.config.DATABASE_URL, 'sqlite:///test.db')

    @patch.dict(os.environ, {'ALGORITHM': 'HS512'})
    def test_algorithm_from_env(self):
        """Testa se ALGORITHM é carregado do ambiente"""
        # Recarrega o módulo para pegar a nova variável de ambiente
        import importlib
        import src.config
        importlib.reload(src.config)
        
        self.assertEqual(src.config.ALGORITHM, 'HS512')


if __name__ == "__main__":
    unittest.main()
