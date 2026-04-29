from pydantic import BaseModel, ConfigDict, Field


class PlantaCadCreate(BaseModel):
    """Schema para criação de planta CAD"""

    tipo: str | None = Field(None, max_length=100)
    arquivo: str | None = Field(None, max_length=255)
    id_projeto: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
