from pydantic import BaseModel, ConfigDict, Field


class ProjetoCreate(BaseModel):
    """Schema para criação de projeto"""
    id_usuario: int | None = Field(None, description="ID do usuário")
    nome: str = Field(..., min_length=1, max_length=150)
    descricao_projeto: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
