from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .usuario import User


class Project(Base):
    __tablename__ = "Projetos"

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    data_criacao: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), init=False, nullable=True
    )
    descricao_projeto: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )
    id_usuario: Mapped[int | None] = mapped_column(
        ForeignKey("Usuario.id"), nullable=True, default=None
    )

    user: Mapped["User | None"] = relationship(
        "User", back_populates="projects", init=False
    )
    model_config = ConfigDict(from_attributes=True)
