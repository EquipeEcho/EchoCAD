from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CalculoCreate(BaseModel):
    """Schema para criação de cálculo"""
    tipo: str | None = Field(None, max_length=100)
    entrada_json: dict[str, Any] | list[Any] | None = Field(None)
    resultado_json: dict[str, Any] | list[Any] | None = Field(None)
    regra_aplicada: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
