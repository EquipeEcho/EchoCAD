from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .especificacoes_tecnicas import EspecificacaoTecnica
    from .memoriais_calculo import MemorialCalculo
    from .norma import Norma
    from .planta_cad import PlantaCad
    from .projeto_norma import ProjetoNorma
    from .projeto_planta import ProjetoPlanta
    from .usuario import Usuario


class Projeto(Base):
    __tablename__ = "Projeto"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    data_criacao: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), init=False, nullable=True
    )
    
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("Usuario.id"), nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    cliente: Mapped[str | None] = mapped_column(String(150), nullable=True, default=None)

    usuario: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="projetos", init=False
    )
    normas: Mapped[List["Norma"]] = relationship(
        "Norma", secondary="Projeto_norma", back_populates="projetos", init=False
    )
    plantas: Mapped[List["PlantaCad"]] = relationship(
        "PlantaCad", secondary="Projeto_planta", back_populates="projetos", init=False
    )
    projeto_normas: Mapped[List["ProjetoNorma"]] = relationship(
        "ProjetoNorma", back_populates="projeto", init=False
    )
    projeto_plantas: Mapped[List["ProjetoPlanta"]] = relationship(
        "ProjetoPlanta", back_populates="projeto", init=False
    )
    especificacoes_tecnicas: Mapped[List["EspecificacaoTecnica"]] = relationship(
        "EspecificacaoTecnica", back_populates="projeto", init=False
    )
    memoriais_calculo: Mapped[List["MemorialCalculo"]] = relationship(
        "MemorialCalculo", back_populates="projeto", init=False
    )
