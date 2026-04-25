from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class DocumentoGerado(Base):
    __tablename__ = "Documentos_gerados"

    tipo_documento: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    caminho_arquivo: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    data_geracao: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), init=False, nullable=True
    )
    model_config = ConfigDict(from_attributes=True)
