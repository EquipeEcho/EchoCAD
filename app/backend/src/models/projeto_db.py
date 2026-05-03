from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class MemorialCalculo(Base):
    """
    Memorial de calculo, Arquivo xlxx com as informações de calculo do projeto
    """
    __tablename__ = "memorial_calculo"

    id: Mapped[int] = mapped_column(primary_key=True) # ok der
    arquivo: Mapped[str] = mapped_column(String(255), nullable=False) # ok der
    
    id_projeto: Mapped[int] = mapped_column(ForeignKey("projeto.id"), nullable=False) # ok deve existir

    projeto: Mapped["Projeto"] = relationship("Projeto", back_populates="memoriais_calculo", init=True) # ok revisado


class PlantaCad(Base):
    """
    Arquivo CAD pertencente ao projeto.
    """
    __tablename__ = "planta_cad"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) # ok der
    tipo: Mapped[str | None] = mapped_column(String(100), nullable=False) # ok der
    arquivo: Mapped[str | None] = mapped_column(String(255), nullable=False) # ok der
    
    id_projeto: Mapped[int] = mapped_column(ForeignKey("projeto.id"), nullable=False) # ok deve existir

    projeto: Mapped["Projeto"] = relationship("Projeto", back_populates="plantas_cad", init=True) # ok revisado


class EspecificacaoTecnica(Base):
    """
    Arquivo de especificação técnica gerado pelo LLM.
    """
    __tablename__ = "especificacao_tecnica"
    id: Mapped[int] = mapped_column(primary_key=True, init=False) # ok def
    arquivo: Mapped[str] = mapped_column(String(255), nullable=False) # ok def

    id_projeto: Mapped[int] = mapped_column(ForeignKey("projeto.id"), nullable=False) # ok deve existir
    projeto: Mapped["Projeto"] = relationship("Projeto", back_populates="especificacoes_tecnicas", init=False)



# isso aqui teria que entrar como RAG / CHROMA, mas vou deixar por enquanto só até implantar o rag
class Norma(Base):
    """
    Representação de uma norma técnica.
    """
    __tablename__ = "normas"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) # ok der
    nome: Mapped[str] = mapped_column(String(150), nullable=False) # ok der

    data_criacao: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), init=False)
    
    projetos: Mapped[List["Projeto"]] = relationship("Projeto", secondary="projeto_norma", back_populates="normas", init=False)


class ProjetoNorma(Base):
    """
    Entidade associativa entre normas e projetos.
    """
    __tablename__ = 'projeto_norma'
    id_norma: Mapped[int] = mapped_column(ForeignKey("normas.id"), primary_key=True, nullable=False) # ok revisado
    id_projeto: Mapped[int] = mapped_column(ForeignKey("projeto.id"), primary_key=True, nullable=False) # ok revisado


# TODO: implementação do usuário para sprint 3
# não será usada por enquanto porque não há sistema de login/cadastro
class Usuario(Base):
    """
    Representa um usuário do sistema.
    """
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) # ok
    nome: Mapped[str] = mapped_column(String(150), nullable=False) # ok
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False) # ok
    senha: Mapped[str] = mapped_column(String(255), nullable=False) # ok
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None) # ok
    
    projetos: Mapped[List["Projeto"]] = relationship("Projeto", back_populates="user", init=False)


class Projeto(Base):
    """
    Representa um registro de projeto na tabela do banco de dodos,
    contém os campos relacioandos à entidade Projeto.
    """
    __tablename__ = "projeto"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) # der
    name: Mapped[str] = mapped_column(String(150), nullable=False) # der
    description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None) # der
    client: Mapped[str | None] = mapped_column(String(150), nullable=True, default=None) # der
    created_at: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now(), init=False) # not der / util

    # revisar essa regra na sprint 3
    id_user: Mapped[int | None] = mapped_column(ForeignKey("usuario.id"), nullable=True, init=True, default=None)

    # TODO: sprint 3
    # usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="projetos", init=False)


    # TODO: implementar com RAG
    # normas: Mapped[List["Norma"]] = relationship("Norma", secondary="Projeto_norma", back_populates="projetos", init=False) # como está isso

    especificacoes_tecnicas: Mapped[List["EspecificacaoTecnica"]] = relationship(
        "EspecificacaoTecnica", back_populates="projeto", init=False
    )

    plantas_cad: Mapped[List['PlantaCad']] = relationship("PlantaCad", back_populates="projeto", init=False) # ok revisado
    memoriais_calculo: Mapped[List["MemorialCalculo"]] = relationship("MemorialCalculo", back_populates="projeto", init=False) # ok revisado
    normas: Mapped[List["Norma"]] = relationship("Norma", secondary="projeto_norma", back_populates="projetos", init=False) # ok revisado
    user: Mapped["Usuario"] = relationship("Usuario", back_populates="projetos", init=False)
