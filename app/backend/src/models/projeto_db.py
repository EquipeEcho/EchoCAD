from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Report(Base):
    """
    Memorial de calculo, Arquivo xlxx com as informações de calculo do projeto
    """
    __tablename__ = "reports"

    id: Mapped[int | None] = mapped_column(primary_key=True, init=False, autoincrement=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="reports", init=False)


class Blueprint(Base):
    """
    Representa o registro de uma planta cad no banco de dados.
    """
    __tablename__ = "blueprints"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    discipline: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="blueprints", init=False)


class Specification(Base):
    """
    Arquivo de especificação técnica gerado pelo LLM.
    """
    __tablename__ = "specifications"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)

    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["Project"] = relationship("Project", back_populates="specifications", init=False)



# isso aqui teria que entrar como RAG / CHROMA, mas vou deixar por enquanto só até implantar o rag
class Standard(Base):
    """
    Representação de uma registro de norma técnica no banco de dados.
    """
    __tablename__ = "standards"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), init=False)
    
    projects: Mapped[List["Project"]] = relationship("Project", secondary="project_standard", back_populates="standards", init=False)


class ProjectStandard(Base):
    """
    Entidade associativa entre normas e projetos.
    """
    __tablename__ = 'project_standard'
    id_standard: Mapped[int] = mapped_column(ForeignKey("standards.id"), primary_key=True, nullable=False)
    id_project: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True, nullable=False)


# TODO: implementação do usuário para sprint 3
# não será usada por enquanto porque não há sistema de login/cadastro
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
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), init=False)
    
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="user", init=False)


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
    created_at: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now(), init=False)

    # revisar essa regra na sprint 3
    id_user: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, init=True, default=None)

    # TODO: sprint 3
    # usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="projetos", init=False)


    # TODO: implementar com RAG
    # normas: Mapped[List["Norma"]] = relationship("Norma", secondary="Projeto_norma", back_populates="projetos", init=False) # como está isso

    specifications: Mapped[List["Specification"]] = relationship(
        "Specification", back_populates="project", init=False
    )

    blueprints: Mapped[List['Blueprint']] = relationship("Blueprint", back_populates="project", init=False)
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="project", init=False)
    standards: Mapped[List["Standard"]] = relationship("Standard", secondary="project_standard", back_populates="projects", init=False)
    user: Mapped["User"] = relationship("User", back_populates="projects", init=False)
