"""
Exceções customizadas para o domínio da aplicação.
Centraliza o tratamento de erros de negócio.
"""


class UserAlreadyExistsError(Exception):
    """Exceção lançada quando tenta criar um usuário com email já existente."""
    pass


class UserNotFoundError(Exception):
    """Exceção lançada quando um usuário não é encontrado."""
    pass


class InvalidCredentialsError(Exception):
    """Exceção lançada quando as credenciais são inválidas."""
    pass


class UnauthorizedOperationError(Exception):
    """Exceção lançada quando uma operação não é autorizada."""
    pass
