from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUser(BaseModel):
    """
    ## Schema Pydantic para criação de usuário.
    ### Campos obrigatórios:
    - name (str): Nome do usuário, obrigatório, com no máximo 100 caracteres.
    - email (EmailStr): E-mail do usuário, obrigatório, com no máximo 150 caracteres.
    - password (str): Senha do usuário, obrigatória, com no mínimo 6 e no máximo 255 caracteres.
    """
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=150)
    password: str = Field(..., min_length=6, max_length=255)
    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    """
    Schema para autenticação de usuário.
    - email (EmailStr): E-mail do usuário, obrigatório, com no máximo 150 caracteres.
    - password (str): Senha do usuário, obrigatória, com no mínimo 6 e no máximo 255 caracteres.
    """
    email: EmailStr = Field(..., max_length=150)
    password: str = Field(..., min_length=6, max_length=255)
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    """Schema para visualização de usuário criados"""
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=150)
    created_at: datetime = Field(...,
                                 description='Data de criação do registro')
    message: str = Field(..., description='Mensagem de resposta da API')

    model_config = ConfigDict(from_attributes=True)


class ProjetcSchema(BaseModel):
    """Schema para criação do projeto"""
    # TODO: implementar a associação com usuário
    id_user: int | None = Field(None)
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description='Nome do projeto'
    )
    description: str | None = Field(
        None, description='Descrição opcional do projeto')
    client: str | None = Field(None)
    model_config = ConfigDict(from_attributes=True, extra='ignore')


class ProjectPublic(ProjetcSchema):
    """Classe para consulta do usuário via GET"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID gerado automaticamente')
    created_at: datetime = Field(...,
                                 description='Data de criação do registro')


class StandardSchema(BaseModel):
    """Schema Pydantic para criação de norma técnica."""

    nome: str = Field(..., min_length=1, max_length=150)
    # conexao: str | None = Field(None, max_length=100)
    # status: str | None = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class BlueprintSchema(BaseModel):
    """Schema para criação de planta CAD"""

    discipline: str | None = Field(None, max_length=100)
    path: str | None = Field(None, max_length=255)
    id_project: int = Field(...)

    model_config = ConfigDict(from_attributes=True)


class BlueprintPublic(BlueprintSchema):
    """Schema para visualização de planta CAD com ID"""
    id: int = Field(..., description='ID gerado automaticamente')
    model_config = ConfigDict(from_attributes=True)


class MemorialCalculoCreate(BaseModel):
    """Schema para criação de memorial de cálculo"""
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class EspecificacaoTecnicaCreate(BaseModel):
    """Schema para criação de especificação técnica"""
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class AssocProjectStandardSchema(BaseModel):
    """Schema para associação projeto-norma"""

    id_projeto: int = Field(...)
    id_norma: int = Field(...)

    model_config = ConfigDict(from_attributes=True)


class CreateProjectBlueprintSchema(BaseModel):
    """Schema para associação projeto-planta"""

    id_projeto: int = Field(...)
    id_planta: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
