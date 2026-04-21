from datetime import datetime
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from typing import TYPE_CHECKING
from pydantic import ConfigDict

if TYPE_CHECKING:
    from .arquivos import Arquivo


class Processamento(Base):
    __tablename__ = 'Processamento'
    Status: Mapped[str] = mapped_column(String(50), nullable=False)
    Data_inicio: Mapped[datetime] = mapped_column(nullable=True)
    Data_fim: Mapped[datetime] = mapped_column(nullable=True)
    Log_erro: Mapped[str] = mapped_column(Text, nullable=True)
    Versao_parser: Mapped[str] = mapped_column(String(50), nullable=True)
    idArquivos: Mapped[int] = mapped_column(ForeignKey('Arquivos.ID'), nullable=False)

    arquivo: Mapped['Arquivo'] = relationship('Arquivo', init=False)
    model_config = ConfigDict(from_attributes=True)