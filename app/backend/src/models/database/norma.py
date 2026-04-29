from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .projeto import Projeto
    from .projeto_norma import ProjetoNorma


class Norma(Base):
    __tablename__ = "Norma"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    conexao: Mapped[str | None] = mapped_column(String(100), nullable=False)
    data_criacao: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), init=False, nullable=True
    )
    
    status: Mapped[str | None] = mapped_column(String(50), nullable=False, default=True)

    projetos: Mapped[List["Projeto"]] = relationship(
        "Projeto", secondary="Projeto_norma", back_populates="normas", init=False
    )
    projeto_normas: Mapped[List["ProjetoNorma"]] = relationship(
        "ProjetoNorma", back_populates="norma", init=False
    )
