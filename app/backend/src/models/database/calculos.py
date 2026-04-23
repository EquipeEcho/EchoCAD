from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base
from pydantic import ConfigDict


class Calculo(Base):
    __tablename__ = 'Calculos'
    Tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    Entrada_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    Resultado_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    Regra_aplicada: Mapped[str] = mapped_column(Text, nullable=False)
    model_config = ConfigDict(from_attributes=True)