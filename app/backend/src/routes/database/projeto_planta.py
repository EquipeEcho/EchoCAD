from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_session
from ...modules.Database.projeto_planta import (
    create_projeto_planta,
    read_all_projeto_planta,
    read_projeto_planta,
)
from ...schemas.database import ProjetoPlantaCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=["projeto_planta"])


@router.post("/", summary="Associar projeto e planta")
async def create_projeto_planta_route(
    projeto_planta: ProjetoPlantaCreate, db: Session = Depends(get_session)
):
    return safe_create(
        create_projeto_planta, db, projeto_planta, "Erro ao associar projeto e planta"
    )


@router.get("/", summary="Listar associações projeto-planta")
async def list_projeto_planta(db: Session = Depends(get_session)):
    return safe_read(
        read_all_projeto_planta, db, "Erro ao buscar associações projeto-planta"
    )


@router.get("/{id_projeto}/{id_planta}", summary="Buscar associação projeto-planta")
async def get_projeto_planta(
    id_projeto: int, id_planta: int, db: Session = Depends(get_session)
):
    return read_projeto_planta(db, id_projeto, id_planta)
