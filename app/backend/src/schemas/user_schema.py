from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Tipos personalizados para validação de campos e aplicação do princípio
# DRY (Don't Repeat Yourself) nos esquemas de usuário.

UserName = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
        description="Nome do usuário"
    )
]

ProjectName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=150,
        description="Nome do projeto"
    )
]

EmailStd = Annotated[
    EmailStr,
    Field(
        min_length=5,
        max_length=100,
        description="Email padrão do sistema"
    )
]

Password = Annotated[
    str,
    Field(
        min_length=6,
        max_length=255,
        description='Senha do usuário (Mínimo 6 e máximo 255 caracteres).'
    )
]


# Schemas para a criação, visualização e atualização de usuários.

class CreateUserSchema(BaseModel):
    """
    ## Schema Pydantic para criação de usuário.
    ### Campos obrigatórios:
    - name (str): Nome do usuário (máximo 100 caracteres), obrigatório.
    - email (EmailStr): E-mail do usuário (máximo 150 caracteres), obrigatório.
    - password (str): Senha do usuário (mínimo 6 e máximo 255 caracteres), obrigatória.
    """

    name: UserName = Field(
        ...,
        description='Nome do usuário (máximo 100 caracteres).')

    email: EmailStd = Field(
        ...,
        description='E-mail do usuário (máximo 150 caracteres).')

    password: Password = Field(
        ...,
        description='Senha do usuário (Mínimo 6 e máximo 255 caracteres).')

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    """
    ## Schema Pydantic para atualização de usuário.
    ### Campos obrigatórios:
    - id (int): ID do usuário a ser atualizado, obrigatório para identificação do registro.
    - password (str): Senha atual do usuário, obrigatória para autenticação da atualização.
    ### Campos opcionais:
    - name (str): Nome do usuário (máximo 100 caracteres), opcional.
    - email (EmailStr): E-mail do usuário (máximo 150 caracteres), opcional.
    - new_password (str): Nova senha do usuário (mínimo 6 e máximo 255 caracteres), opcional.
    """

    id: int = Field(..., description='ID do usuário a ser atualizado.')

    name: UserName | None = Field(
        None,
        description='Novo nome do usuário (Opcional, máximo 100 caracteres).')

    email: EmailStd | None = Field(
        None,
        description='Novo e-mail do usuário (Opcional, máximo 150 caracteres).')

    password: Password = Field(
        ...,
        description='Senha atual do usuário.')

    new_password: Password | None = Field(
        None,
        description='Nova senha do usuário (Opcional, mínimo 6 e máximo 255 caracteres).')

    model_config = ConfigDict(from_attributes=True)


class LoginUserSchema(BaseModel):
    """
    ## Schema para autenticação de usuário.
    ### Campos obrigatórios:
    - email (EmailStr): E-mail do usuário, obrigatório, com no máximo 150 caracteres.
    - password (str): Senha do usuário, obrigatória, com no mínimo 6 e no máximo 255 caracteres.
    """

    email: EmailStd = Field(
        ...,
        description='E-mail do usuário (Obrigatório, máximo 150 caracteres).')

    password: Password = Field(
        ...,
        description='Senha do usuário (Obrigatória, mínimo 6 e máximo 255 caracteres).')

    model_config = ConfigDict(from_attributes=True)


class UserPublicSchema(BaseModel):
    """
    ## Schema para visualização de usuário criados

    ### Campos obrigatórios:
    - name (str): Nome do usuário, obrigatório, com no máximo 100 caracteres.
    - email (EmailStr): E-mail do usuário, obrigatório, com no máximo 150 caracteres.
    - created_at (datetime): Data de criação do registro.
    - message (str): Mensagem de resposta da API.
    """

    name: UserName = Field(
        ...,
        description='Nome do usuário (máximo 100 caracteres).')

    email: EmailStd = Field(
        ...,
        description='E-mail do usuário (máximo 150 caracteres).')

    created_at: datetime = Field(
        ...,
        description='Data de criação do registro')

    message: str = Field(
        ...,
        description='Mensagem de resposta da API')

    model_config = ConfigDict(from_attributes=True)


# Schemas para criação, visualização e atualização de projetos.

class CreateProjectSchema(BaseModel):
    """
    ## Schema para criação do projeto
    ### Campos obrigatórios:
    - name (str): Nome do projeto (mínimo 1 e no máximo 150 caracteres).
    ### Campos opcionais:
    - description (str): Descrição do projeto, opcional.
    - client (str): Nome do cliente, opcional.
    """

    # TODO: verificar a associação de usuários e projetos
    id_user: int | None = Field(None)

    name: ProjectName = Field(
        ...,
        description='Nome do projeto (entre 1 e 150 caracteres).')

    description: str | None = Field(
        None, description='Descrição opcional do projeto')

    client: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class ProjectPublicSchema(CreateProjectSchema):
    """
    Schema para resposta de criação do projeto.
    ### Campos obrigatórios:
    - id_project (int): Id único gerado para o projeto.
    - name (str): Nome do projeto (entre 1 e 150 caracteres).
    - created_at (datetime): Data de criação do registro.
    """

    id: int = Field(..., description='Id do projeto criado.')

    name: ProjectName = Field(
        ...,
        description='Nome do projeto criado.')

    created_at: datetime = Field(
        ...,
        description='Datetime (UTC) de criação do projeto.')

    model_config = ConfigDict(from_attributes=True)


class UpdateProjectSchema(BaseModel):
    """
    ## Schema para atualização do projeto
    ### Campos opcionais:
    - name (str): Nome do projeto (mínimo 1 e no máximo 150 caracteres).
    - description (str): Descrição do projeto, opcional.
    - client (str): Nome do cliente, opcional.
    """

    name: ProjectName | None = Field(
        None,
        description='Novo nome do projeto (entre 1 e 150 caracteres).')

    description: str | None = Field(
        None, description='Nova descrição do projeto, opcional.')

    client: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class DeleteProjectSchema(BaseModel):
    """
    ## Schema para exclusão do projeto
    ### Campos obrigatórios:
    - id (int): ID do projeto a ser excluído.
    """

    # TODO: implementar autenticação para a exclusão de projetos.
    id: int = Field(..., description='ID do projeto a ser excluído.')

    model_config = ConfigDict(from_attributes=True)


# Schema para criação, visualização e atualização de normas técnicas.

class StandardSchema(BaseModel):
    """Schema Pydantic para criação de norma técnica."""

    nome: str = Field(..., min_length=1, max_length=150)
    # conexao: str | None = Field(None, max_length=100)
    # status: str | None = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)

# Schemas para criação, visualização e atualização de plantas CAD.


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


# Schema para visualização de memorial de cálculo.


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
