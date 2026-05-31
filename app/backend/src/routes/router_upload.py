# Standard Library (Bibliotecas nativas)
import aiofiles
import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.auth import get_current_user

from src.schemas.system_schema import UploadResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])

# definindo local de salvamento dos arquivos
BACKEND_ROOT = Path(__file__).parent.parent.parent
DEFAULT_PATH = BACKEND_ROOT / "uploads"
DEFAULT_PATH.mkdir(parents=True, exist_ok=True)


@router.post(
    "/{project_id}", status_code=status.HTTP_201_CREATED, response_model=UploadResponse
)
async def upload(
    project_id: int,
    current_user=Depends(get_current_user),
    file: UploadFile = File(...),
):
    """
    Rota para upload de arquivos.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome do arquivo é requerido",
        )

    # Validar extensão do arquivo
    allowed_suffixes = {".dxf", ".pdf", ".doc", ".docx"}
    if Path(file.filename).suffix.lower() not in allowed_suffixes:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Formato nao suportado. Envie arquivos DXF, PDF, DOC ou DOCX.",
        )

    try:
        project_path = DEFAULT_PATH / str(project_id)
        project_path.mkdir(parents=True, exist_ok=True)

        safe_name = Path(file.filename).name
        file_path = (project_path / safe_name).resolve()
        try:
            file_path.relative_to(project_path.resolve())
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de arquivo inválido.",
            ) from exc

        content = await file.read()
        # Salvar arquivo no disco
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(content)

        # Retornamos o caminho relativo para ser salvo no banco
        relative_path = f"{project_id}/{file.filename}"

    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar arquivo: {str(e)}",
        )
    finally:
        await file.close()

    return {
            "message": "Upload realizado com sucesso",
            "filename": file.filename,
            "path": relative_path,
        }
