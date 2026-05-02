# src/routes/especificacoes.py
# Rota FastAPI para geração de especificações técnicas a partir de arquivo DXF.

import hashlib
import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from src.database import get_session
from src.controller.file_controller import save_file_metadata
from src.modules.EspecificacoesTecnicas import gerar_especificacoes

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/especificacoes",
    tags=["especificacoes"],
)

UPLOAD_DIR  = Path("uploads")
OUTPUT_DIR  = Path("outputs/especificacoes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXTENSOES_VALIDAS = {".dxf", ".dwg"}


# ---------------------------------------------------------------------------
# POST /especificacoes/
# Recebe um arquivo DXF e gera as especificações técnicas em .docx
# ---------------------------------------------------------------------------
@router.post(
    "/",
    summary="Gerar especificações técnicas a partir de arquivo DXF",
    response_description="Arquivo .docx com o caderno de especificações técnicas",
)
async def gerar_especificacoes_route(
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    # ---- Validação ----
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome do arquivo é requerido.",
        )

    extensao = Path(file.filename).suffix.lower()
    if extensao not in EXTENSOES_VALIDAS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Formato não suportado. Use {', '.join(EXTENSOES_VALIDAS)}.",
        )

    # ---- Salvar arquivo ----
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Hash para integridade
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        file_hash = h.hexdigest()
        file_size = file_path.stat().st_size

        # Persistir metadados (não-bloqueante em erro)
        try:
            saved = save_file_metadata(db, file.filename, file_size, file_hash)
            logger.info(f"Metadados salvos: {file.filename} (ID: {saved.id})")
        except Exception as db_err:
            logger.warning(f"Falha ao salvar metadados: {db_err}")

        # ---- Gerar especificações ----
        stem = Path(file.filename).stem
        nome_projeto = stem.replace("_", " ").replace("-", " ").title()
        output_path  = OUTPUT_DIR / f"especificacoes_{stem}.docx"

        logger.info(f"Gerando especificações para: {nome_projeto}")

        arquivo_gerado = gerar_especificacoes(
            dxf_file=str(file_path),
            output_path=str(output_path),
            nome_projeto=nome_projeto,
        )

        # Retornar o arquivo gerado
        media_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if arquivo_gerado.suffix == ".docx"
            else "text/plain"
        )

        return FileResponse(
            path=str(arquivo_gerado),
            filename=arquivo_gerado.name,
            media_type=media_type,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar especificações: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar arquivo: {str(e)}",
        )


# ---------------------------------------------------------------------------
# GET /especificacoes/contexto/
# Retorna apenas o contexto extraído do DXF (útil para debug/preview)
# ---------------------------------------------------------------------------
@router.post(
    "/contexto",
    summary="Extrair e retornar contexto do DXF (sem gerar documento)",
    response_class=JSONResponse,
)
async def extrair_contexto_route(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome do arquivo é requerido.",
        )

    extensao = Path(file.filename).suffix.lower()
    if extensao not in EXTENSOES_VALIDAS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Formato não suportado. Use {', '.join(EXTENSOES_VALIDAS)}.",
        )

    try:
        from src.modules.EspecificacoesTecnicas import DXFContextExtractor

        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        nome_projeto = Path(file.filename).stem.replace("_", " ").title()
        extractor = DXFContextExtractor(str(file_path), nome_projeto=nome_projeto)
        ctx = extractor.extrair()

        return JSONResponse(content=ctx.to_dict())

    except Exception as e:
        logger.error(f"Erro ao extrair contexto: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )