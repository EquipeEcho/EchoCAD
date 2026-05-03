from pydantic import BaseModel, ConfigDict, Field


class EspecificacaoTecnicaCreate(BaseModel):
    """Schema para criação de especificação técnica"""
    arquivo: str | None = Field(None, max_length=255)
    melhorias: str | None = Field(None)
    versao: int | None = Field(1)
    id_projeto: int = Field(...)
    id_antigo: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
