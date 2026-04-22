from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Project (Base):
    __tablename__ = 'projects'
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False)

    description: Mapped[str | None] = mapped_column(String(50), nullable=True)

    user: Mapped['User'] = relationship(
        'User', back_populates='projects', init=False)
