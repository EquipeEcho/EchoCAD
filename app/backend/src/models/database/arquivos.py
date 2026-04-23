from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from typing import TYPE_CHECKING
from pydantic import ConfigDict

if TYPE_CHECKING:
    from .projeto import Project
    from .calculos import Calculo
    from .documentos_gerados import DocumentoGerado
    from .elementos import Elemento


class Arquivo(Base):
    __tablename__ = 'Arquivos'
    Caminho: Mapped[str] = mapped_column(String(255), nullable=False)
    Nome_arquivo: Mapped[str] = mapped_column(String(150), nullable=False)
    Tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    idProjetos: Mapped[int] = mapped_column(ForeignKey('Projetos.ID'), nullable=True)
    idCalculos: Mapped[int] = mapped_column(ForeignKey('Calculos.ID'), nullable=True)
    idDocumentos_gerados: Mapped[int] = mapped_column(ForeignKey('Documentos_gerados.ID'), nullable=True)
    idElementos: Mapped[int] = mapped_column(ForeignKey('Elementos.ID'), nullable=True)

    project: Mapped['Project'] = relationship('Project', init=False)
    calculo: Mapped['Calculo'] = relationship('Calculo', init=False)
    documento: Mapped['DocumentoGerado'] = relationship('DocumentoGerado', init=False)
    elemento: Mapped['Elemento'] = relationship('Elemento', init=False)
    model_config = ConfigDict(from_attributes=True)