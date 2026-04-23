from pydantic import BaseModel, ConfigDict, Field


class MemorialCalculoCreate(BaseModel):
    """Schema para criação de memorial de cálculo"""
    idDocumentos_gerados: int = Field(...)
    idCalculos: int = Field(...)
    Resultados: str = Field(...)
    Norma_referencia: str = Field(..., max_length=150)
    Observacoes: str | None = Field(None)
    
    model_config = ConfigDict(from_attributes=True)