from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCreate(BaseModel):
    """Schema para criação de usuário"""
    Nome: str = Field(..., max_length=100)
    Email: EmailStr = Field(..., max_length=150)
    Senha: str = Field(..., max_length=255)
    
    model_config = ConfigDict(from_attributes=True)