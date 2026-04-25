from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .calculos import Calculo
    from .documentos_gerados import DocumentoGerado


class MemorialCalculo(Base):
    __tablename__ = "Memoriais_calculo"

    id_documentos_gerados: Mapped[int | None] = mapped_column(
        ForeignKey("Documentos_gerados.id"), nullable=True, default=None
    )
    id_calculos: Mapped[int | None] = mapped_column(
        ForeignKey("Calculos.id"), nullable=True, default=None
    )
    resultados: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    norma_referencia: Mapped[str | None] = mapped_column(
        String(150), nullable=True, default=None
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    documento: Mapped["DocumentoGerado | None"] = relationship(
        "DocumentoGerado", init=False
    )
    calculo: Mapped["Calculo | None"] = relationship("Calculo", init=False)
    model_config = ConfigDict(from_attributes=True)
