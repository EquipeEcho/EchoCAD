from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .projeto import Projeto
    from .projeto_planta import ProjetoPlanta


class PlantaCad(Base):
    __tablename__ = "Planta_cad"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    tipo: Mapped[str | None] = mapped_column(String(100), nullable=False)
    arquivo: Mapped[str | None] = mapped_column(String(255), nullable=False)
    
    id_projeto: Mapped[int] = mapped_column(ForeignKey("Projeto.id"), nullable=False)

    projeto: Mapped["Projeto"] = relationship("Projeto", init=False)
    projetos: Mapped[List["Projeto"]] = relationship(
        "Projeto", secondary="Projeto_planta", back_populates="plantas", init=False
    )
    projeto_plantas: Mapped[List["ProjetoPlanta"]] = relationship(
        "ProjetoPlanta", back_populates="planta", init=False
    )
