from sqlalchemy.orm import Session
from src.models import (
    User, Project, ComandoIA, DocumentoGerado, EspecificacaoTecnica,
    Calculo, MemorialCalculo, Elemento, Arquivo, Coordenada, Processamento
)
from src.schemas import (
    CreateUser, ProjectCreate, ComandoIACreate, DocumentoGeradoCreate,
    EspecificacaoTecnicaCreate, CalculoCreate, MemorialCalculoCreate,
    ElementoCreate, ArquivoCreate, CoordenadaCreate, ProcessamentoCreate
)


def create_usuario(db: Session, user: CreateUser):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_projeto(db: Session, project: ProjectCreate):
    new_project = Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def create_comando_ia(db: Session, comando: ComandoIACreate):
    new_comando = ComandoIA(**comando.model_dump())
    db.add(new_comando)
    db.commit()
    db.refresh(new_comando)
    return new_comando


def create_documento_gerado(db: Session, documento: DocumentoGeradoCreate):
    new_documento = DocumentoGerado(**documento.model_dump())
    db.add(new_documento)
    db.commit()
    db.refresh(new_documento)
    return new_documento


def create_especificacao_tecnica(db: Session, espec: EspecificacaoTecnicaCreate):
    new_espec = EspecificacaoTecnica(**espec.model_dump())
    db.add(new_espec)
    db.commit()
    db.refresh(new_espec)
    return new_espec


def create_calculo(db: Session, calc: CalculoCreate):
    new_calc = Calculo(**calc.model_dump())
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc


def create_memorial_calculo(db: Session, memorial: MemorialCalculoCreate):
    new_memorial = MemorialCalculo(**memorial.model_dump())
    db.add(new_memorial)
    db.commit()
    db.refresh(new_memorial)
    return new_memorial


def create_elemento(db: Session, elem: ElementoCreate):
    new_elem = Elemento(**elem.model_dump())
    db.add(new_elem)
    db.commit()
    db.refresh(new_elem)
    return new_elem


def create_arquivo(db: Session, arquivo: ArquivoCreate):
    new_arquivo = Arquivo(**arquivo.model_dump())
    db.add(new_arquivo)
    db.commit()
    db.refresh(new_arquivo)
    return new_arquivo


def create_coordenada(db: Session, coord: CoordenadaCreate):
    new_coord = Coordenada(**coord.model_dump())
    db.add(new_coord)
    db.commit()
    db.refresh(new_coord)
    return new_coord


def create_processamento(db: Session, proc: ProcessamentoCreate):
    new_proc = Processamento(**proc.model_dump())
    db.add(new_proc)
    db.commit()
    db.refresh(new_proc)
    return new_proc