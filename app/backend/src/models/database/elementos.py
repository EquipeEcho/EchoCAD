from decimal import Decimal

from pydantic import ConfigDict
from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class Elemento(Base):
    __tablename__ = "Elementos"

    layer: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    geometria: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    comprimento: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 2), nullable=True, default=None
    )
    area: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 2), nullable=True, default=None
    )
    categoria_tecnica_tipo: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    model_config = ConfigDict(from_attributes=True)
