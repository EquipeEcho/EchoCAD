from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from typing import TYPE_CHECKING
from pydantic import ConfigDict

if TYPE_CHECKING:
    from .documentos_gerados import DocumentoGerado
    from .calculos import Calculo


class MemorialCalculo(Base):
    __tablename__ = 'Memoriais_Calculo'
    idDocumentos_gerados: Mapped[int] = mapped_column(ForeignKey('Documentos_gerados.ID'), nullable=False)
    idCalculos: Mapped[int] = mapped_column(ForeignKey('Calculos.ID'), nullable=False)
    Resultados: Mapped[str] = mapped_column(Text, nullable=False)
    Norma_referencia: Mapped[str] = mapped_column(String(150), nullable=False)
    Observacoes: Mapped[str] = mapped_column(Text, nullable=True)

    documento: Mapped['DocumentoGerado'] = relationship('DocumentoGerado', init=False)
    calculo: Mapped['Calculo'] = relationship('Calculo', init=False)
    model_config = ConfigDict(from_attributes=True)