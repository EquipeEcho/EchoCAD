from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base
from pydantic import ConfigDict


class Elemento(Base):
    __tablename__ = 'Elementos'
    Layer: Mapped[str] = mapped_column(String(100), nullable=False)
    Geometria: Mapped[str] = mapped_column(String(100), nullable=False)
    Comprimento: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    Area: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    Categoria_tecnica_tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    model_config = ConfigDict(from_attributes=True)