from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ComandoIACreate(BaseModel):
    """Schema para criação de comando IA"""
    comando_original: str | None = Field(None)
    intencao_detectada: str | None = Field(None, max_length=255)
    parametros_extraidos: dict[str, Any] | list[Any] | None = Field(None)
    id_usuario: int | None = Field(None)
    id_projetos: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
