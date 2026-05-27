import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from src.database import get_session
from src.modules.EspecificacoesTecnicas import gerar_especificacoes
from src.controller.specification_controller import criar_especificacao

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/especificacoes",
    tags=["especificacoes"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs/especificacoes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXTENSOES_VALIDAS = {".dxf", ".dwg"}


@router.post(
    "/",
    summary="Gerar especificações técnicas a partir de arquivo DXF",
    response_description="Arquivo .docx com o caderno de especificações técnicas",
)
async def gerar_especificacoes_route(
    file: UploadFile = File(...),
    id_project: int = Form(...),
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

    try:
        # ---- Salvar arquivo DXF fisicamente para a extração ----
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---- Gerar especificações ----
        stem = Path(file.filename).stem
        nome_projeto = stem.replace("_", " ").replace("-", " ").title()
        output_path = OUTPUT_DIR / f"especificacoes_{stem}.docx"

        logger.info(f"Gerando especificações para: {nome_projeto}")

        arquivo_gerado = gerar_especificacoes(
            dxf_file=str(file_path),
            output_path=str(output_path),
            nome_projeto=nome_projeto,
        )

        # ---- Salvar no banco de dados ----
        try:
            criar_especificacao(db=db, path=str(arquivo_gerado), id_project=id_project)
            logger.info(
                f"Especificação gerada e vinculada ao projeto {id_project} com sucesso."
            )
        except Exception as db_err:
            logger.error(
                f"Erro ao salvar a instância da especificação no banco: {db_err}"
            )

        # ---- Retornar o arquivo gerado ----
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
