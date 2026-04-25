from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUser(BaseModel):
    """Schema para criação de usuário"""
    nome: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=150)
    senha: str = Field(..., max_length=255)

    model_config = ConfigDict(from_attributes=True)
