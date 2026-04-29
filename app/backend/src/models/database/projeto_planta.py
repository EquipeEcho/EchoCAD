from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .planta_cad import PlantaCad
    from .projeto import Projeto


class ProjetoPlanta(Base):
    __tablename__ = "Projeto_planta"

    id_projeto: Mapped[int] = mapped_column(
        ForeignKey("Projeto.id"), primary_key=True, init=False
    )
    id_planta: Mapped[int] = mapped_column(
        ForeignKey("Planta_cad.id"), primary_key=True, init=False
    )

    projeto: Mapped["Projeto"] = relationship(
        "Projeto", back_populates="projeto_plantas", init=False
    )
    planta: Mapped["PlantaCad"] = relationship(
        "PlantaCad", back_populates="projeto_plantas", init=False
    )
