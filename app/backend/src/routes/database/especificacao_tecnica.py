from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.especificacao_tecnica import create_especificacao_tecnica, read_especificacao_tecnica, read_all_especificacoes_tecnicas
from ...schemas.database import EspecificacaoTecnicaCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['especificacao_tecnica'])


@router.post('/', summary='Criar especificação técnica')
async def create_especificacao(espec: EspecificacaoTecnicaCreate, db: Session = Depends(get_session)):
    return safe_create(create_especificacao_tecnica, db, espec, "Erro ao criar especificação técnica")


@router.get('/', summary='Listar todas as especificações técnicas')
async def list_especificacoes(db: Session = Depends(get_session)):
    return safe_read(read_all_especificacoes_tecnicas, db, "Erro ao buscar especificações técnicas")


@router.get('/{especificacao_id}', summary='Buscar especificação técnica por ID')
async def get_especificacao(especificacao_id: int, db: Session = Depends(get_session)):
    return read_especificacao_tecnica(db, especificacao_id)