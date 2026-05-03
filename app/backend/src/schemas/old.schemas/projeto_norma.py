from pydantic import BaseModel, ConfigDict, Field


class ProjetoNormaCreate(BaseModel):
    """Schema para associação projeto-norma"""

    id_projeto: int = Field(...)
    id_norma: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
