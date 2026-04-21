from sqlalchemy import ForeignKey, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from typing import TYPE_CHECKING
from pydantic import ConfigDict

if TYPE_CHECKING:
    from .elementos import Elemento


class Coordenada(Base):
    __tablename__ = 'Coordenadas'
    idElementos: Mapped[int] = mapped_column(ForeignKey('Elementos.ID'), nullable=False)
    X: Mapped[float] = mapped_column(DECIMAL(10,4), nullable=False)
    Y: Mapped[float] = mapped_column(DECIMAL(10,4), nullable=False)
    Ordem: Mapped[int] = mapped_column(Integer, nullable=False)

    elemento: Mapped['Elemento'] = relationship('Elemento', init=False)
    model_config = ConfigDict(from_attributes=True)