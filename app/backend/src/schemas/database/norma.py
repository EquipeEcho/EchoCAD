from pydantic import BaseModel, ConfigDict, Field


class NormaCreate(BaseModel):
    """Schema para criação de norma"""

    nome: str = Field(..., min_length=1, max_length=150)
    conexao: str | None = Field(None, max_length=100)
    status: str | None = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)
