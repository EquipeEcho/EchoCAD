from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .norma import Norma
    from .projeto import Projeto


class ProjetoNorma(Base):
    __tablename__ = "Projeto_norma"

    id_projeto: Mapped[int] = mapped_column(
        ForeignKey("Projeto.id"), primary_key=True, init=False
    )
    id_norma: Mapped[int] = mapped_column(
        ForeignKey("Norma.id"), primary_key=True, init=False
    )

    projeto: Mapped["Projeto"] = relationship(
        "Projeto", back_populates="projeto_normas", init=False
    )
    norma: Mapped["Norma"] = relationship(
        "Norma", back_populates="projeto_normas", init=False
    )
