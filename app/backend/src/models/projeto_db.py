from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Report(Base):
    """
    Memorial de calculo, Arquivo xlxx com as informações de calculo do projeto
    """

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project: Mapped["Project"] = relationship(
        "Project", back_populates="reports", init=False, lazy="selectin"
    )


class Blueprint(Base):
    """
    Representa o registro de uma planta cad no banco de dados.
    """

    __tablename__ = "blueprints"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    discipline: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)

    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project: Mapped["Project"] = relationship(
        "Project", back_populates="blueprints", init=False, lazy="selectin"
    )


class Specification(Base):
    """
    Arquivo de especificação técnica gerado pelo LLM.
    """

    __tablename__ = "specifications"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)

    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["Project"] = relationship(
        "Project", back_populates="specifications", init=False, lazy="selectin"
    )


class Standard(Base):
    """
    Representação de uma registro de norma técnica no banco de dados.
    """

    __tablename__ = "standards"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), init=False
    )

    projects: Mapped[List["Project"]] = relationship(
        "Project",
        secondary="project_standard",
        back_populates="standards",
        init=False,
        lazy="selectin",
    )


class ProjectStandard(Base):
    """
    Entidade associativa entre normas e projetos.
    """

    __tablename__ = "project_standard"
    id_standard: Mapped[int] = mapped_column(
        ForeignKey("standards.id"), primary_key=True, nullable=False
    )
    id_project: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), primary_key=True, nullable=False
    )


class User(Base):
    """
    Representa um usuário do sistema.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    groq_api_key_encrypted: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None, repr=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), init=False
    )

    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="user", init=False, lazy="selectin"
    )


class Project(Base):
    """
    Representa um registro de projeto na tabela do banco de dodos,
    contém os campos relacioandos à entidade Projeto.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    client: Mapped[str | None] = mapped_column(String(150), nullable=True, default=None)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), init=False
    )

    id_user: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, init=True, default=None
    )

    specifications: Mapped[List["Specification"]] = relationship(
        "Specification", back_populates="project", init=False, lazy="selectin"
    )

    blueprints: Mapped[List["Blueprint"]] = relationship(
        "Blueprint", back_populates="project", init=False, lazy="selectin"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report", back_populates="project", init=False, lazy="selectin"
    )
    standards: Mapped[List["Standard"]] = relationship(
        "Standard",
        secondary="project_standard",
        back_populates="projects",
        init=False,
        lazy="selectin",
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="projects", init=False, lazy="selectin"
    )
