import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from src.auth import get_current_user

from src.controller.crud_blueprints import create_blueprint, read_all_blueprints
from src.database import get_async_session
from src.schemas.user_schema import BlueprintSchema, BlueprintPublic
from src.modules.drill import processar_dxf

router = APIRouter(prefix="/planta_cad", tags=["planta_cad"])

BACKEND_ROOT = Path(__file__).resolve().parents[2]
UPLOADS_DIR = BACKEND_ROOT / "uploads"


@router.post(
    "/",
    summary="Criar planta CAD",
    status_code=status.HTTP_201_CREATED,
    response_model=BlueprintPublic,
)
async def route_create_blueprint(
    planta: BlueprintSchema,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Rota para adicionar uma planta de CAD no banco de dados.
    """
    try:
        result = await create_blueprint(db, planta)
        return result

    except Exception as e:
        msg = "Erro ao adicionar planta cad"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/", summary="Listar plantas CAD", status_code=status.HTTP_200_OK)
async def list_blueprints(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Rota para listar todas as plantas CAD do projeto.
    """
    try:
        result = await read_all_blueprints(db)
        return result

    except Exception as e:
        msg = "Erro ao buscar as plantas existentes"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/extrair", summary="Extrai dados do .DXF", status_code=status.HTTP_200_OK)
async def extrair_dxf(
    caminho: str,
    current_user=Depends(get_current_user),
):
    try:
        # 1. Valida que o caminho é relativo e permanece dentro de UPLOADS_DIR
        safe_path = Path(caminho.replace("\\", "/"))
        if safe_path.is_absolute() or ".." in safe_path.parts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Caminho inválido.",
            )

        uploads_root = UPLOADS_DIR.resolve()
        file_path = (uploads_root / safe_path).resolve()

        try:
            file_path.relative_to(uploads_root)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Caminho fora da pasta de uploads.",
            ) from exc

        # 2. Verifica se o arquivo existe
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo .DXF não encontrado no caminho especificado.",
            )

        # 3. Executa processamento CPU-bound em thread separada
        relatorio_json = await asyncio.to_thread(processar_dxf, str(file_path))
        return relatorio_json

    except HTTPException:
        raise
    except Exception as e:
        msg = "Erro ao extrair dados do .DXF"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")
