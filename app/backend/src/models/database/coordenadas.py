from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .elementos import Elemento


class Coordenada(Base):
    __tablename__ = "Coordenadas"

    id_elementos: Mapped[int | None] = mapped_column(
        ForeignKey("Elementos.id"), nullable=True, default=None
    )
    x: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 4), nullable=True, default=None
    )
    y: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 4), nullable=True, default=None
    )
    ordem: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)

    elemento: Mapped["Elemento | None"] = relationship("Elemento", init=False)
    model_config = ConfigDict(from_attributes=True)
