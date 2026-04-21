from pydantic import BaseModel, ConfigDict, Field


class DocumentoGeradoCreate(BaseModel):
    """Schema para criação de documento gerado"""
    Tipo_documento: str = Field(..., max_length=100)
    Caminho_arquivo: str = Field(..., max_length=255)
    
    model_config = ConfigDict(from_attributes=True)