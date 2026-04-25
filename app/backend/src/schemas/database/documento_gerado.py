from pydantic import BaseModel, ConfigDict, Field


class DocumentoGeradoCreate(BaseModel):
    """Schema para criação de documento gerado"""
    tipo_documento: str | None = Field(None, max_length=100)
    caminho_arquivo: str | None = Field(None, max_length=255)

    model_config = ConfigDict(from_attributes=True)
