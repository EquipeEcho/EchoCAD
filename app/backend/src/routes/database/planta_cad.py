from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_session
from ...modules.Database.planta_cad import (
    create_planta_cad,
    read_all_plantas_cad,
    read_planta_cad,
)
from ...schemas.database import PlantaCadCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=["planta_cad"])


@router.post("/", summary="Criar planta CAD")
async def create_planta_route(planta: PlantaCadCreate, db: Session = Depends(get_session)):
    return safe_create(create_planta_cad, db, planta, "Erro ao criar planta CAD")


@router.get("/", summary="Listar plantas CAD")
async def list_plantas(db: Session = Depends(get_session)):
    return safe_read(read_all_plantas_cad, db, "Erro ao buscar plantas CAD")


@router.get("/{planta_id}", summary="Buscar planta CAD por ID")
async def get_planta(planta_id: int, db: Session = Depends(get_session)):
    return read_planta_cad(db, planta_id)
