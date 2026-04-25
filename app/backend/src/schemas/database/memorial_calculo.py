from pydantic import BaseModel, ConfigDict, Field


class MemorialCalculoCreate(BaseModel):
    """Schema para criação de memorial de cálculo"""
    id_documentos_gerados: int | None = Field(None)
    id_calculos: int | None = Field(None)
    resultados: str | None = Field(None)
    norma_referencia: str | None = Field(None, max_length=150)
    observacoes: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
