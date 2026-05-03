from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.controller.planta_crud import create_planta_cad, read_all_plantas_cad
from src.database import get_session
from src.schemas.user_schema import PlantaSchema


router = APIRouter(prefix='/planta_cad', tags=["planta_cad"])


@router.post("/", summary="Criar planta CAD")
async def create_planta_route(planta: PlantaSchema, db: Session = Depends(get_session)):
    """
    Rota para adicionar uma planta de CAD no banco de dados.
    """
    try:
        result = create_planta_cad(db, planta)
        return ({'object': result.arquivo, 'message': "Planta registrada com sucesso."})

    except Exception as e:
        msg = 'Erro ao adicionar planta cad'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/", summary="Listar plantas CAD")
async def list_plantas(db: Session = Depends(get_session)):
    """
    Rota para listar todas as plantas CAD do projeto.
    """
    try:
        result = read_all_plantas_cad(db)
        return result

    except Exception as e:
        msg = 'Erro ao buscar as plantas existentes'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


# revisar depois
# @router.get("/{planta_id}", summary="Buscar planta CAD por ID")
# async def get_planta(planta_id: int, db: Session = Depends(get_session)):
#     return read_planta_cad(db, planta_id)
