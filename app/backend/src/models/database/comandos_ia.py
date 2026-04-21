from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import ForeignKey, String, Text, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .usuario import User
    from .projeto import Project


class ComandoIA(Base):
    __tablename__ = 'Comandos_IA'
    Comando_original: Mapped[str] = mapped_column(Text, nullable=False)
    Intencao_detectada: Mapped[str] = mapped_column(String(255), nullable=False)
    Parametros_extraidos: Mapped[dict] = mapped_column(JSON, nullable=False)
    Data: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    idUsuario: Mapped[int] = mapped_column(ForeignKey('Usuario.ID'), nullable=False)
    idProjetos: Mapped[int] = mapped_column(ForeignKey('Projetos.ID'), nullable=False)

    user: Mapped['User'] = relationship('User', init=False)
    project: Mapped['Project'] = relationship('Project', init=False)
    model_config = ConfigDict(from_attributes=True)