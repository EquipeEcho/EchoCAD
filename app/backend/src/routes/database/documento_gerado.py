from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.documento_gerado import create_documento_gerado, read_documento_gerado, read_all_documentos_gerados
from ...schemas.database import DocumentoGeradoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['documento_gerado'])


@router.post('/', summary='Criar documento gerado')
async def create_documento(documento: DocumentoGeradoCreate, db: Session = Depends(get_session)):
    return safe_create(create_documento_gerado, db, documento, "Erro ao criar documento gerado")


@router.get('/', summary='Listar todos os documentos gerados')
async def list_documentos(db: Session = Depends(get_session)):
    return safe_read(read_all_documentos_gerados, db, "Erro ao buscar documentos gerados")


@router.get('/{documento_id}', summary='Buscar documento gerado por ID')
async def get_documento(documento_id: int, db: Session = Depends(get_session)):
    return read_documento_gerado(db, documento_id)