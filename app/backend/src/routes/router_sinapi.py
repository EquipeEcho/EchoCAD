from pathlib import Path
import os
import aiofiles
import aiofiles.os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth import get_current_user
from src.config import settings

UPLOAD_DIR = settings.SINAPI_UPLOAD_DIR

router = APIRouter(
    prefix="/sinapi", 
    tags=["sinapi"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all():
    """listar todos os arquivos sinapi existentes"""
    if not os.path.exists(UPLOAD_DIR):
        return {"files": []}
    files = [f.name for f in Path(UPLOAD_DIR).iterdir() if f.is_file()]
    return {"files": files}


@router.post("", status_code=status.HTTP_201_CREATED)
async def post(file: UploadFile = File(...)):
    """inserir a sinapi no sistema"""
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum arquivo válido foi enviado ou o nome do arquivo está vazio",
        )
    
    if not file.filename.endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extensão de arquivo não permitida.",
        )

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

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
        "saved_path": str(file_path),
    }


@router.put("", status_code=status.HTTP_200_OK)
async def put(filename: str, file: UploadFile = File(...)):
    """atualizar a sinapi existente"""
    file_path = Path(UPLOAD_DIR).joinpath(filename)
    
    if not await aiofiles.os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado.",
        )

    try:
        contents = await file.read()
        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar o arquivo: {str(e)}",
        )
    finally:
        await file.close()

    return {"message": f"Arquivo {filename} atualizado com sucesso."}


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete(filename: str = Query(...)):
    """remover a sinapi do sistema"""
    file_path = Path(UPLOAD_DIR).joinpath(filename)
    
    if not await aiofiles.os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado.",
        )
    
    try:
        await aiofiles.os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover o arquivo: {str(e)}",
        )

