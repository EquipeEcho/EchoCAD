from typing import Any

from pydantic import ConfigDict
from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class Calculo(Base):
    __tablename__ = "Calculos"

    tipo: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    entrada_json: Mapped[Any | None] = mapped_column(JSON, nullable=True, default=None)
    resultado_json: Mapped[Any | None] = mapped_column(
        JSON, nullable=True, default=None
    )
    regra_aplicada: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    model_config = ConfigDict(from_attributes=True)
