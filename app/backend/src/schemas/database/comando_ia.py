from pydantic import BaseModel, ConfigDict, Field


class ComandoIACreate(BaseModel):
    """Schema para criação de comando IA"""
    Comando_original: str = Field(...)
    Intencao_detectada: str = Field(..., max_length=255)
    Parametros_extraidos: dict = Field(...)
    idUsuario: int = Field(...)
    idProjetos: int = Field(...)
    
    model_config = ConfigDict(from_attributes=True)