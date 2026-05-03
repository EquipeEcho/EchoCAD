from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUser(BaseModel):
    """Validar a criação do usuário via POST"""
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=150)
    senha: str = Field(..., max_length=255)
    cargo: str | None = Field(None, max_length=100)
    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    """Schema para autenticação de usuário"""
    email: EmailStr = Field(..., max_length=150)
    senha: str = Field(..., min_length=1, max_length=255)
    model_config = ConfigDict(from_attributes=True)


class ProjetoSchema(BaseModel):
    """Classe de validação da criação do modelo via POST"""
    # id_usuario: int = Field(..., description='ID do usuário')
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description='Nome do projeto'
    )
    description: str | None = Field(
        None, description='Descrição opcional do projeto')
    model_config = ConfigDict(from_attributes=True)


class ProjectPublic(ProjetoSchema):
    """Classe para consulta do usuário via GET"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID gerado automaticamente')
    created_at: datetime = Field(...,
                                 description='Data de criação do registro')
