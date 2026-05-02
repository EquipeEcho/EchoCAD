# Standard Library (Bibliotecas nativas)
import hashlib
import logging
import shutil
from pathlib import Path

# Third Party (Bibliotecas instaladas - ex: FastAPI, SQLAlchemy)
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# Local Application (Módulos internos do seu projeto)
from src.controller.file_controller import save_file_metadata
from src.database import get_session



logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)

# definindo local de salvamento dos arquivos
DEFAULT_PATH = Path('uploads')
DEFAULT_PATH.mkdir(parents=True, exist_ok=True)


@router.post('/')
async def upload(file: UploadFile = File(...), db: Session = Depends(get_session)):
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
        file_path = DEFAULT_PATH.joinpath(file.filename)
        
        # Salvar arquivo no disco
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Calcular hash SHA-256 do arquivo
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        file_hash = hash_sha256.hexdigest()
        
        # Obter tamanho do arquivo
        file_size = file_path.stat().st_size

        # Salvar metadados no banco de dados
        try:
            saved_file = save_file_metadata(db, file.filename, file_size, file_hash)
            logger.info(f"Metadados salvos para {file.filename} (ID: {saved_file.id})")
        except Exception as db_err:
            logger.error(f"Erro ao salvar metadados: {db_err}")

        basepath = Path("src/modules/memorial")

        template_file = (basepath / "model_memorial.xlsx").resolve()

        output_file = (basepath / f"memorial_{Path(file.filename).stem}.xlsx").resolve()
        logger.info(output_file)

        run_integration(
            dxf_file=str(file_path),
            template_file=str(template_file),
            output_file=str(output_file)
        )

        return FileResponse(
            path=output_file, 
            filename=f"memorial_{file.filename}.xlsx",
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Erro ao processar arquivo: {str(e)}'
        )