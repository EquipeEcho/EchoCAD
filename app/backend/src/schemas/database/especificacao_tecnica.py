from pydantic import BaseModel, ConfigDict, Field


class EspecificacaoTecnicaCreate(BaseModel):
    """Schema para criação de especificação técnica"""
    idDocumentos_gerados: int = Field(...)
    Categoria_tecnica: str = Field(..., max_length=100)
    Descricao: str = Field(...)
    Materiais_previstos: str = Field(...)
    Norma_referencia: str = Field(..., max_length=150)
    Observacoes: str | None = Field(None)
    
    model_config = ConfigDict(from_attributes=True)