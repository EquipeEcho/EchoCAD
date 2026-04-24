from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.arquivo import create_arquivo, read_arquivo, read_all_arquivos
from ...schemas.database import ArquivoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['arquivo'])


@router.post('/', summary='Criar arquivo')
async def create_arq(arquivo: ArquivoCreate, db: Session = Depends(get_session)):
    return safe_create(create_arquivo, db, arquivo, "Erro ao criar arquivo")


@router.get('/', summary='Listar todos os arquivos')
async def list_arquivos(db: Session = Depends(get_session)):
    return safe_read(read_all_arquivos, db, "Erro ao buscar arquivos")


@router.get('/{arquivo_id}', summary='Buscar arquivo por ID')
async def get_arquivo(arquivo_id: int, db: Session = Depends(get_session)):
    return read_arquivo(db, arquivo_id)