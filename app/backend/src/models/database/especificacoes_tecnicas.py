from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .documentos_gerados import DocumentoGerado


class EspecificacaoTecnica(Base):
    __tablename__ = "Especificacoes_tecnicas"

    id_documentos_gerados: Mapped[int | None] = mapped_column(
        ForeignKey("Documentos_gerados.id"), nullable=True, default=None
    )
    categoria_tecnica: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    materiais_previstos: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )
    norma_referencia: Mapped[str | None] = mapped_column(
        String(150), nullable=True, default=None
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    documento: Mapped["DocumentoGerado | None"] = relationship(
        "DocumentoGerado", init=False
    )
    model_config = ConfigDict(from_attributes=True)
