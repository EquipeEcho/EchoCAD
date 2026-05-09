from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from controller.crud_blueprints import create_blueprint, read_all_blueprints
from src.database import get_session
from src.schemas.system_schema import Success
from src.schemas.user_schema import BlueprintSchema, BlueprintPublic


router = APIRouter(prefix='/planta_cad', tags=["planta_cad"])


@router.post("/", summary="Criar planta CAD", status_code=status.HTTP_201_CREATED, response_model=BlueprintPublic)
async def route_create_blueprint(planta: BlueprintSchema, db: Session = Depends(get_session)):
    """
    Rota para adicionar uma planta de CAD no banco de dados.
    """
    try:
        result = create_blueprint(db, planta)
        return result

    except Exception as e:
        msg = 'Erro ao adicionar planta cad'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/", summary="Listar plantas CAD", status_code=status.HTTP_200_OK)
async def list_blueprints(db: Session = Depends(get_session)):
    """
    Rota para listar todas as plantas CAD do projeto.
    """
    try:
        result = read_all_blueprints(db)
        return result

    except Exception as e:
        msg = 'Erro ao buscar as plantas existentes'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")
