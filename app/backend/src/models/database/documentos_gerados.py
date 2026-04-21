from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class DocumentoGerado(Base):
    __tablename__ = 'Documentos_gerados'
    Tipo_documento: Mapped[str] = mapped_column(String(100), nullable=False)
    Caminho_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    Data_geracao: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    model_config = ConfigDict(from_attributes=True)