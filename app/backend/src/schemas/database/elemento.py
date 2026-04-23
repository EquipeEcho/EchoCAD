from pydantic import BaseModel, ConfigDict, Field


class ElementoCreate(BaseModel):
    """Schema para criação de elemento"""
    Layer: str = Field(..., max_length=100)
    Geometria: str = Field(..., max_length=100)
    Comprimento: float = Field(...)
    Area: float = Field(...)
    Categoria_tecnica_tipo: str = Field(..., max_length=100)
    
    model_config = ConfigDict(from_attributes=True)