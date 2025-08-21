from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Schemas para a API (validação de entrada e saída)


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int

    # ✅ SOLUÇÃO: ConfigDict moderno para Pydantic V2
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
