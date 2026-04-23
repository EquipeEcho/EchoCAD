from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProcessamentoCreate(BaseModel):
    """Schema para criação de processamento"""
    Status: str = Field(..., max_length=50)
    Data_inicio: datetime | None = Field(None)
    Data_fim: datetime | None = Field(None)
    Log_erro: str | None = Field(None)
    Versao_parser: str | None = Field(None, max_length=50)
    idArquivos: int = Field(...)
    
    model_config = ConfigDict(from_attributes=True)