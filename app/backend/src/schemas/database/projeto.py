from pydantic import BaseModel, ConfigDict, Field


class ProjetoCreate(BaseModel):
    """Schema para criação de projeto"""
    idUsuario: int = Field(..., description='ID do usuário')
    Nome: str = Field(..., min_length=1, max_length=150)
    Descricao_projeto: str | None = Field(None)
    
    model_config = ConfigDict(from_attributes=True)