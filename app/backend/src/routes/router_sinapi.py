from pathlib import Path
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

UPLOAD_DIR = "./sinapi"

router = APIRouter(prefix="/sinapi", tags=["sinapi"])


@router.get("/sinapi", status_code=status.HTTP_200_OK)
async def get():
    """obter a sinapi atual"""
    pass


@router.post("/sinapi", status_code=status.HTTP_201_CREATED)
async def post(file: UploadFile = File(...)):
    """inserir a sinapi no sistema"""
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum arquivo válido foi enviado ou o nome do arquivo está vazio",
        )
    else:
        if not file.filename.endswith((".xlsx", ".xls", ".csv")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Extensão de arquivo não permitida.",
            )

        file_path = Path(UPLOAD_DIR).joinpath(file.filename)

        try:
            contents = await file.read()

            async with aiofiles.open(file_path, "wb") as out_file:
                await out_file.write(contents)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar o arquivo: {str(e)}",
            )
        finally:
            await file.close()

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "saved_path": file_path,
        }


@router.put("", status_code=status.HTTP_200_OK)
async def put():
    """atualizar a sinapi existente"""
    pass


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete():
    """remover a sinapi do sistema"""
    pass
