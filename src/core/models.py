from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    """
    Modelo de domínio representando um usuário.
    Esta é a entidade central do nosso negócio.
    """

    id: int
    username: str
    email: EmailStr
    hashed_password: str

    # ✅ SOLUÇÃO: ConfigDict moderno para Pydantic V2
    model_config = ConfigDict(from_attributes=True)
