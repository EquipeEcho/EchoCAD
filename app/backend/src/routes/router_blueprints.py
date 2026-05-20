from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from pathlib import Path

from src.controller.crud_blueprints import create_blueprint, read_all_blueprints
from src.database import get_session
from src.schemas.system_schema import Success
from src.schemas.user_schema import BlueprintSchema, BlueprintPublic
from src.modules.core.build.drill import processar_dxf

router = APIRouter(prefix="/planta_cad", tags=["planta_cad"])


@router.post(
    "/",
    summary="Criar planta CAD",
    status_code=status.HTTP_201_CREATED,
    response_model=BlueprintPublic,
)
async def route_create_blueprint(
    planta: BlueprintSchema, db: Session = Depends(get_session)
):
    """
    Rota para adicionar uma planta de CAD no banco de dados.
    """
    try:
        result = create_blueprint(db, planta)
        return result

    except Exception as e:
        msg = "Erro ao adicionar planta cad"
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
        msg = "Erro ao buscar as plantas existentes"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/", summary="Extrai dados do .DXF", status_code=status.HTTP_200_OK)
async def Extrator_DXF(Caminho: str):
    try:
        # Define o caminho do DXF
        pasta_do_script = Path(__file__).parent
        caminho = Caminho

        if not Path(caminho).exists():
            print("Coloque o caminho do .DXF")
        # 2. Roda o motor passando as configurações dinâmicas
        relatorio_json = processar_dxf(caminho)
        return relatorio_json
    except Exception as e:
        msg = "Erro ao extrair dados do .DXF"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")
