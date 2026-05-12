from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field


UserName = Annotated[
    str,
    Field(min_length=2, max_length=100, description="Nome do usuario")
]

ProjectName = Annotated[
    str,
    Field(min_length=1, max_length=150, description="Nome do projeto")
]

EmailStd = Annotated[
    EmailStr,
    Field(min_length=5, max_length=100, description="Email padrao do sistema")
]

Password = Annotated[
    str,
    Field(min_length=6, max_length=255, description="Senha do usuario")
]

Role = Annotated[
    str,
    Field(min_length=2, max_length=100, description="Cargo do usuario")
]


class CreateUserSchema(BaseModel):
    name: UserName = Field(..., description="Nome do usuario")
    email: EmailStd = Field(..., description="E-mail do usuario")
    password: Password = Field(..., description="Senha do usuario")
    role: Role | None = Field(None, description="Cargo do usuario")

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    id: int = Field(..., description="ID do usuario a ser atualizado")
    name: UserName | None = Field(None, description="Novo nome do usuario")
    email: EmailStd | None = Field(None, description="Novo e-mail do usuario")
    password: Password = Field(..., description="Senha atual do usuario")
    new_password: Password | None = Field(None, description="Nova senha do usuario")

    model_config = ConfigDict(from_attributes=True)


class LoginUserSchema(BaseModel):
    email: EmailStd = Field(..., description="E-mail do usuario")
    password: Password = Field(..., description="Senha do usuario")

    model_config = ConfigDict(from_attributes=True)


class UserPublicSchema(BaseModel):
    id: int = Field(..., description="ID do usuario")
    name: UserName = Field(..., description="Nome do usuario")
    email: EmailStd = Field(..., description="E-mail do usuario")
    role: Role | None = Field(None, description="Cargo do usuario")
    created_at: datetime = Field(..., description="Data de criacao do registro")
    message: str = Field(..., description="Mensagem de resposta da API")

    model_config = ConfigDict(from_attributes=True)


class CreateProjectSchema(BaseModel):
    id_user: int = Field(..., description="ID do usuario criador do projeto")
    name: ProjectName = Field(..., description="Nome do projeto")
    description: str | None = Field(None, description="Descricao opcional do projeto")
    client: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class ProjectPublicSchema(CreateProjectSchema):
    """
    Schema para resposta de criacao do projeto.
    ### Campos obrigatorios:
    - id_project (int): Id unico gerado para o projeto.
    - name (str): Nome do projeto (entre 1 e 150 caracteres).
    - created_at (datetime): Data de criacao do registro.
    """

    id: int = Field(..., description='Id do projeto criado.')

    name: ProjectName = Field(
        ...,
        description='Nome do projeto criado.')

    created_at: datetime = Field(
        ...,
        description='Datetime (UTC) de criacao do projeto.')

    model_config = ConfigDict(from_attributes=True)


class UpdateProjectSchema(BaseModel):
    """
    Schema para atualizar um projeto existente.
    ### Campos obrigatorios:
    - id (int): ID do projeto a ser atualizado.
    ### Campos opcionais:
    - name (str): Novo nome do projeto (entre 1 e 150 caracteres).
    - description (str): Nova descricao do projeto.
    - client (str): Novo cliente do projeto.
    """
    id: int = Field(..., description="ID do projeto a ser atualizado")
    name: ProjectName | None = Field(None, description="Novo nome do projeto")
    description: str | None = Field(None, description="Nova descricao do projeto")
    client: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class DeleteProjectSchema(BaseModel):
    id: int = Field(..., description="ID do projeto a ser excluido")

    model_config = ConfigDict(from_attributes=True)


class StandardSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)

    model_config = ConfigDict(from_attributes=True)


class BlueprintSchema(BaseModel):
    discipline: str | None = Field(None, max_length=100)
    path: str | None = Field(None, max_length=255)
    id_project: int = Field(...)

    model_config = ConfigDict(from_attributes=True)


class BlueprintPublic(BlueprintSchema):
    id: int = Field(..., description="ID gerado automaticamente")

    model_config = ConfigDict(from_attributes=True)


class MemorialCalculoCreate(BaseModel):
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class EspecificacaoTecnicaCreate(BaseModel):
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class AssocProjectStandardSchema(BaseModel):
    id_projeto: int = Field(...)
    id_norma: int = Field(...)

    model_config = ConfigDict(from_attributes=True)


class CreateProjectBlueprintSchema(BaseModel):
    id_projeto: int = Field(...)
    id_planta: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
