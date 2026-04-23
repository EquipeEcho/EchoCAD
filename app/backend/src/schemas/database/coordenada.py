from pydantic import BaseModel, ConfigDict, Field


class CoordenadaCreate(BaseModel):
    """Schema para criação de coordenada"""
    idElementos: int = Field(...)
    X: float = Field(...)
    Y: float = Field(...)
    Ordem: int = Field(...)
    
    model_config = ConfigDict(from_attributes=True)