from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas.system_schema import Success
from src.schemas.user_schema import NormaSchema

from src.controller.norma_crud import create_norma, read_all_normas

router = APIRouter(prefix='/norma', tags=["norma"])


@router.post("/", summary="Criar norma", status_code=status.HTTP_201_CREATED, response_model=Success)
async def create_norma_route(norma_schema: NormaSchema, db: Session = Depends(get_session)):
    """
    Rota adição de uma nova norma técnica.
    """
    try:
        result = create_norma(db, norma_schema)
        return ({'object': result.nome, 'message': "Adicionado com sucesso ao registro."})

    except Exception as e:
        msg = 'Erro ao adicionar norma técnica'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get("/", summary="Listar todas as normas", status_code=status.HTTP_200_OK)
async def list_normas(db: Session = Depends(get_session)):
    try:
        result = read_all_normas(db)
        return result

    except Exception as e:
        msg = 'Erro ao buscar os projetos existentes'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


# VER DEPOis
# @router.get("/{norma_id}", summary="Buscar norma por ID")
# async def get_norma(norma_id: int, db: Session = Depends(get_session)):
#     return read_norma(db, norma_id)
