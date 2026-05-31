from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field


UserName = Annotated[
    str, Field(min_length=2, max_length=100, description="Nome do usuario")
]

ProjectName = Annotated[
    str, Field(min_length=1, max_length=150, description="Nome do projeto")
]

EmailStd = Annotated[
    EmailStr, Field(min_length=5, max_length=100, description="Email padrao do sistema")
]

Password = Annotated[
    str, Field(min_length=6, max_length=255, description="Senha do usuario")
]

Role = Annotated[
    str, Field(min_length=2, max_length=100, description="Cargo do usuario")
]


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseSchema):
    name: UserName = Field(..., description="Nome do usuario")
    email: EmailStd = Field(..., description="E-mail do usuario")
    password: Password = Field(..., description="Senha do usuario")
    role: Role | None = Field(None, description="Cargo do usuario")


class UpdateUserSchema(BaseSchema):
    id: int = Field(..., description="ID do usuario a ser atualizado")
    name: UserName | None = Field(None, description="Novo nome do usuario")
    email: EmailStd | None = Field(None, description="Novo e-mail do usuario")
    password: Password = Field(..., description="Senha atual do usuario")
    new_password: Password | None = Field(None, description="Nova senha do usuario")


class ChangePasswordSchema(BaseSchema):
    current_password: Password = Field(..., description="Senha atual do usuario")
    new_password: Password = Field(..., description="Nova senha do usuario")


class GroqApiKeyUpdateSchema(BaseSchema):
    api_key: str = Field(
        ..., min_length=8, max_length=255, description="Chave da API Groq"
    )


class GroqApiKeyStatusSchema(BaseSchema):
    configured: bool = Field(..., description="Indica se o usuario possui chave Groq")
    masked_key: str | None = Field(None, description="Chave mascarada para exibicao")
    message: str = Field(..., description="Mensagem de resposta da API")


class LoginUserSchema(BaseSchema):
    email: EmailStd = Field(..., description="E-mail do usuario")
    password: Password = Field(..., description="Senha do usuario")


class UserPublicSchema(BaseSchema):
    id: int = Field(..., description="ID do usuario")
    name: UserName = Field(..., description="Nome do usuario")
    email: EmailStd = Field(..., description="E-mail do usuario")
    role: Role | None = Field(None, description="Cargo do usuario")
    created_at: datetime = Field(..., description="Data de criacao do registro")
    message: str = Field(..., description="Mensagem de resposta da API")


class TokenResponseSchema(BaseSchema):
    access_token: str = Field(..., description="JWT de acesso do usuário")
    token_type: str = Field("bearer", description="Tipo de token")
    user: UserPublicSchema = Field(
        ..., description="Dados públicos do usuário autenticado"
    )


class CreateProjectSchema(BaseSchema):
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

    id: int = Field(..., description="Id do projeto criado.")

    name: ProjectName = Field(..., description="Nome do projeto criado.")

    created_at: datetime = Field(
        ..., description="Datetime (UTC) de criacao do projeto."
    )


class UpdateProjectSchema(BaseSchema, extra="ignore"):
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


class DeleteProjectSchema(BaseSchema):
    id: int = Field(..., description="ID do projeto a ser excluido")


class StandardSchema(BaseSchema):
    nome: str = Field(..., min_length=1, max_length=150)


class BlueprintSchema(BaseSchema):
    discipline: str | None = Field(None, max_length=100)
    path: str | None = Field(None, max_length=255)
    id_project: int = Field(...)


class BlueprintPublic(BlueprintSchema):
    id: int = Field(..., description="ID gerado automaticamente")


class MemorialCalculoCreate(BaseSchema):
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)


class EspecificacaoTecnicaCreate(BaseSchema):
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)


class AssocProjectStandardSchema(BaseSchema):
    id_projeto: int = Field(...)
    id_norma: int = Field(...)


class CreateProjectBlueprintSchema(BaseSchema):
    id_projeto: int = Field(...)
    id_planta: int = Field(...)


class AIProviderToggleSchema(BaseSchema):
    """Toggle simples: apenas um boolean"""
    use_ollama: bool = Field(
        ..., 
        description="True para usar Ollama, False para usar Groq"
    )
    
class AIProviderStatusSchema(BaseSchema):
    """Status da configuração de IA"""
    use_ollama: bool
    provider_name: str  # "ollama" ou "groq"
    configured: bool    # True se provider está disponível/configurado
    message: str
