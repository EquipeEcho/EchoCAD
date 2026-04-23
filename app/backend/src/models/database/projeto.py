from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .usuario import User


class Project (Base):
    __tablename__ = 'Projetos'
    idUsuario: Mapped[int | None] = mapped_column(
        ForeignKey('Usuario.ID', ondelete='SET NULL'), nullable=True)

    Nome: Mapped[str] = mapped_column(String(150), nullable=False)

    Data_criacao: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False)

    Descricao_projeto: Mapped[str | None] = mapped_column(nullable=True)

    user: Mapped['User'] = relationship(
        'User', back_populates='projects', init=False)
    model_config = ConfigDict(from_attributes=True)
