from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CoordenadaCreate(BaseModel):
    """Schema para criação de coordenada"""
    id_elementos: int | None = Field(None)
    x: Decimal | None = Field(None)
    y: Decimal | None = Field(None)
    ordem: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
