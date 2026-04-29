from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_session
from ...modules.Database.projeto_norma import (
    create_projeto_norma,
    read_all_projeto_norma,
    read_projeto_norma,
)
from ...schemas.database import ProjetoNormaCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=["projeto_norma"])


@router.post("/", summary="Associar projeto e norma")
async def create_projeto_norma_route(
    projeto_norma: ProjetoNormaCreate, db: Session = Depends(get_session)
):
    return safe_create(
        create_projeto_norma, db, projeto_norma, "Erro ao associar projeto e norma"
    )


@router.get("/", summary="Listar associações projeto-norma")
async def list_projeto_norma(db: Session = Depends(get_session)):
    return safe_read(
        read_all_projeto_norma, db, "Erro ao buscar associações projeto-norma"
    )


@router.get("/{id_projeto}/{id_norma}", summary="Buscar associação projeto-norma")
async def get_projeto_norma(
    id_projeto: int, id_norma: int, db: Session = Depends(get_session)
):
    return read_projeto_norma(db, id_projeto, id_norma)
