from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUser(BaseModel):
    """Schema para criação de usuário"""
    nome: str = Field(..., max_length=150)
    email: EmailStr = Field(..., max_length=150)
    senha: str = Field(..., max_length=255)
    cargo: str | None = Field(None, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    """Schema para autenticação de usuário"""
    email: EmailStr = Field(..., max_length=150)
    senha: str = Field(..., min_length=1, max_length=255)

    model_config = ConfigDict(from_attributes=True)
