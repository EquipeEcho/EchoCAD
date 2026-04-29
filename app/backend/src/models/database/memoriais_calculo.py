from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .projeto import Projeto


class MemorialCalculo(Base):
    __tablename__ = "Memorial_calculo"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    arquivo: Mapped[str | None] = mapped_column(String(255), nullable=False)

    id_projeto: Mapped[int] = mapped_column(ForeignKey("Projeto.id"), nullable=False)
    id_antigo: Mapped[int | None] = mapped_column(
        ForeignKey("Memorial_calculo.id"), nullable=True, default=None
    )

    versao: Mapped[int | None] = mapped_column(Integer, nullable=False, default=1)
    melhorias: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    projeto: Mapped["Projeto"] = relationship(
        "Projeto", back_populates="memoriais_calculo", init=False
    )
    antigo: Mapped["MemorialCalculo | None"] = relationship(
        "MemorialCalculo",
        remote_side="MemorialCalculo.id",
        init=False,
    )
