from typing import TYPE_CHECKING, List

from pydantic import ConfigDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .projeto import Project


class User(Base):
    __tablename__ = 'Usuario'
    Nome: Mapped[str] = mapped_column(String(100), nullable=False)
    Email: Mapped[str] = mapped_column(String(150), unique=True)
    Senha: Mapped[str] = mapped_column(String(255), nullable=False)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="user", init=False)
    model_config = ConfigDict(from_attributes=True)
