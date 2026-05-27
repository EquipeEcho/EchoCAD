from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_user
from src.database import get_async_session
from src.schemas.system_schema import Success
from src.schemas.user_schema import StandardSchema

from src.controller.crud_standards import (
    create_standard,
    read_all_standards,
    toggle_standard_status,
)

router = APIRouter(prefix="/norma", tags=["norma"])


@router.post(
    "/",
    summary="Criar norma",
    status_code=status.HTTP_201_CREATED,
    response_model=Success,
)
async def route_create_standards(
    norma_schema: StandardSchema,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Rota adição de uma nova norma técnica.
    """
    try:
        result = await create_standard(db, norma_schema)
        return {"object": result.name, "message": "Adicionado com sucesso ao registro."}

    except Exception as e:
        msg = "Erro ao adicionar norma técnica"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/", summary="Listar todas as normas", status_code=status.HTTP_200_OK)
async def list_standards(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    try:
        result = await read_all_standards(db)
        return result

    except Exception as e:
        msg = "Erro ao buscar os projetos existentes"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.patch(
    "/toggle",
    summary="Ativar/Desativar norma",
    status_code=status.HTTP_200_OK,
)
async def toggle_standard(
    standard_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Alterna o status de ativa/inativa de uma norma técnica.
    """
    try:
        updated_standard = await toggle_standard_status(db, standard_id)
        return {
            "id": updated_standard.id,
            "nome": updated_standard.name,
            "ativo": updated_standard.active,
            "message": f"Norma {'ativada' if updated_standard.active else 'desativada'} com sucesso.",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        msg = "Erro ao atualizar norma"
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")
