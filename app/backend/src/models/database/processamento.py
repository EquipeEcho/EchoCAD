from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .arquivos import Arquivo


class Processamento(Base):
    __tablename__ = "Processamento"

    status: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    data_inicio: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )
    data_fim: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )
    log_erro: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    versao_parser: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )
    id_arquivos: Mapped[int | None] = mapped_column(
        ForeignKey("Arquivos.id"), nullable=True, default=None
    )

    arquivo: Mapped["Arquivo | None"] = relationship("Arquivo", init=False)
    model_config = ConfigDict(from_attributes=True)
