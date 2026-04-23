from pydantic import BaseModel, ConfigDict, Field


class ArquivoCreate(BaseModel):
    """Schema para criação de arquivo"""
    Caminho: str = Field(..., max_length=255)
    Nome_arquivo: str = Field(..., max_length=150)
    Tipo: str = Field(..., max_length=50)
    idProjetos: int | None = Field(None)
    idCalculos: int | None = Field(None)
    idDocumentos_gerados: int | None = Field(None)
    idElementos: int | None = Field(None)
    
    model_config = ConfigDict(from_attributes=True)