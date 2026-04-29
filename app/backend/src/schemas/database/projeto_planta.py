from pydantic import BaseModel, ConfigDict, Field


class ProjetoPlantaCreate(BaseModel):
    """Schema para associação projeto-planta"""

    id_projeto: int = Field(...)
    id_planta: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
