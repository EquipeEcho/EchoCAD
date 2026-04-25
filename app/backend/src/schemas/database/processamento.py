from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProcessamentoCreate(BaseModel):
    """Schema para criação de processamento"""
    status: str | None = Field(None, max_length=50)
    data_inicio: datetime | None = Field(None)
    data_fim: datetime | None = Field(None)
    log_erro: str | None = Field(None)
    versao_parser: str | None = Field(None, max_length=50)
    id_arquivos: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
