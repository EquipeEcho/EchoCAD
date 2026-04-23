from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_documento_gerado
from ...schemas.database import DocumentoGeradoCreate
from ..helpers import safe_create

router = APIRouter(tags=['documento_gerado'])


@router.post('/', summary='Criar documento gerado')
async def create_documento(documento: DocumentoGeradoCreate, db: Session = Depends(get_session)):
    return safe_create(create_documento_gerado, db, documento, "Erro ao criar documento gerado")