from pydantic import BaseModel, ConfigDict, Field


class ArquivoCreate(BaseModel):
    """Schema para criação de arquivo"""
    caminho: str | None = Field(None, max_length=255)
    nome_arquivo: str | None = Field(None, max_length=150)
    tipo: str | None = Field(None, max_length=50)
    id_projetos: int | None = Field(None)
    id_calculos: int | None = Field(None)
    id_documentos_gerados: int | None = Field(None)
    id_elementos: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
