from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ElementoCreate(BaseModel):
    """Schema para criação de elemento"""
    layer: str | None = Field(None, max_length=100)
    geometria: str | None = Field(None, max_length=100)
    comprimento: Decimal | None = Field(None)
    area: Decimal | None = Field(None)
    categoria_tecnica_tipo: str | None = Field(None, max_length=100)

    model_config = ConfigDict(from_attributes=True)
