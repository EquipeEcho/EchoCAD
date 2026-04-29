from pydantic import BaseModel, ConfigDict, Field


class ProjetoCreate(BaseModel):
    """Schema para criação de projeto"""
    id_usuario: int = Field(..., description="ID do usuário")
    nome: str = Field(..., min_length=1, max_length=150)
    descricao: str | None = Field(None)
    cliente: str | None = Field(None, max_length=150)

    model_config = ConfigDict(from_attributes=True)
