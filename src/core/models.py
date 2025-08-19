from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    Modelo de domínio representando um usuário.
    Esta é a entidade central do nosso negócio.
    """

    id: int
    username: str
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True
