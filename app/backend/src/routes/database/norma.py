from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_session
from ...modules.Database.norma import create_norma, read_all_normas, read_norma
from ...schemas.database import NormaCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=["norma"])


@router.post("/", summary="Criar norma")
async def create_norma_route(norma: NormaCreate, db: Session = Depends(get_session)):
    return safe_create(create_norma, db, norma, "Erro ao criar norma")


@router.get("/", summary="Listar todas as normas")
async def list_normas(db: Session = Depends(get_session)):
    return safe_read(read_all_normas, db, "Erro ao buscar normas")


# VER DEPOis
# @router.get("/{norma_id}", summary="Buscar norma por ID")
# async def get_norma(norma_id: int, db: Session = Depends(get_session)):
#     return read_norma(db, norma_id)
