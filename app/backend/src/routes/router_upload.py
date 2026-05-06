# Standard Library (Bibliotecas nativas)
import logging
import shutil
from pathlib import Path

# Third Party (Bibliotecas instaladas - ex: FastAPI, SQLAlchemy)
from fastapi import APIRouter, File, HTTPException, UploadFile, status

# Local Application (Módulos internos do seu projeto)
# from src.controller.file_controller import save_file_metadata
# from src.database import get_session
from src.schemas.system_schema import UploadResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)

# definindo local de salvamento dos arquivos
BACKEND_ROOT = Path(__file__).parent.parent.parent
DEFAULT_PATH = BACKEND_ROOT / 'uploads'
DEFAULT_PATH.mkdir(parents=True, exist_ok=True)

# TODO: implementar inteligência de separação do tipo de arquivo.
@router.post('/{project_id}', status_code=status.HTTP_201_CREATED, response_model=UploadResponse)
async def upload(project_id: int, file: UploadFile = File(...)):
    """
    Rota para upload de arquivos.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Nome do arquivo é requerido'
        )

    # Validar extensão do arquivo
    if not file.filename.lower().endswith(('dxf', 'pdf', 'doc', 'docx')):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='Formato não suportado.'
        )

    try:
        project_path = DEFAULT_PATH / str(project_id)
        project_path.mkdir(parents=True, exist_ok=True)
        
        file_path = project_path.joinpath(file.filename)

        # Salvar arquivo no disco
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Retornamos o caminho relativo para ser salvo no banco
        relative_path = f"{project_id}/{file.filename}"

        return {
            "message": "Upload realizado com sucesso",
            "filename": file.filename,
            "path": relative_path
        }

    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Erro ao processar arquivo: {str(e)}'
        )
