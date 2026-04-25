from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .calculos import Calculo
    from .documentos_gerados import DocumentoGerado
    from .elementos import Elemento
    from .projeto import Project


class Arquivo(Base):
    __tablename__ = "Arquivos"

    caminho: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    nome_arquivo: Mapped[str | None] = mapped_column(
        String(150), nullable=True, default=None
    )
    tipo: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    id_projetos: Mapped[int | None] = mapped_column(
        ForeignKey("Projetos.id"), nullable=True, default=None
    )
    id_calculos: Mapped[int | None] = mapped_column(
        ForeignKey("Calculos.id"), nullable=True, default=None
    )
    id_documentos_gerados: Mapped[int | None] = mapped_column(
        ForeignKey("Documentos_gerados.id"), nullable=True, default=None
    )
    id_elementos: Mapped[int | None] = mapped_column(
        ForeignKey("Elementos.id"), nullable=True, default=None
    )

    projeto: Mapped["Project | None"] = relationship("Project", init=False)
    calculo: Mapped["Calculo | None"] = relationship("Calculo", init=False)
    documento: Mapped["DocumentoGerado | None"] = relationship(
        "DocumentoGerado", init=False
    )
    elemento: Mapped["Elemento | None"] = relationship("Elemento", init=False)
    model_config = ConfigDict(from_attributes=True)
