from pydantic import BaseModel, ConfigDict, Field


class EspecificacaoTecnicaCreate(BaseModel):
    """Schema para criação de especificação técnica"""
    id_documentos_gerados: int | None = Field(None)
    categoria_tecnica: str | None = Field(None, max_length=100)
    descricao: str | None = Field(None)
    materiais_previstos: str | None = Field(None)
    norma_referencia: str | None = Field(None, max_length=150)
    observacoes: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
