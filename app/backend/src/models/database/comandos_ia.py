from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict
from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .projeto import Project
    from .usuario import User


class ComandoIA(Base):
    __tablename__ = "Comandos_ia"

    comando_original: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )
    intencao_detectada: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    parametros_extraidos: Mapped[Any | None] = mapped_column(
        JSON, nullable=True, default=None
    )
    data: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), init=False, nullable=True
    )
    id_usuario: Mapped[int | None] = mapped_column(
        ForeignKey("Usuario.id"), nullable=True, default=None
    )
    id_projetos: Mapped[int | None] = mapped_column(
        ForeignKey("Projetos.id"), nullable=True, default=None
    )

    user: Mapped["User | None"] = relationship("User", init=False)
    project: Mapped["Project | None"] = relationship("Project", init=False)
    model_config = ConfigDict(from_attributes=True)
