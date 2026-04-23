from pydantic import BaseModel, ConfigDict, Field


class CalculoCreate(BaseModel):
    """Schema para criação de cálculo"""
    Tipo: str = Field(..., max_length=100)
    Entrada_json: dict = Field(...)
    Resultado_json: dict = Field(...)
    Regra_aplicada: str = Field(...)
    
    model_config = ConfigDict(from_attributes=True)