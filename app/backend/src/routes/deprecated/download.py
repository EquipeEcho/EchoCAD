from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os
from src.database import get_session
from src.models.projeto_db import Report, Project

router = APIRouter()

@router.get("/download/xlsx")
def download_xlsx():
    """Rota legada para download de memorial padrão."""
    file_path = "app/backend/src/modules/Memorial/memorial_preenchido.xlsx"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(
        path=file_path,
        filename="memorial.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.get("/download/memorial/{project_id}")
async def download_memorial_by_project(
    project_id: int,
    memorial_id: int = Query(None, description="ID específico do memorial (opcional)"),
    db: Session = Depends(get_session)
):
    """
    Download de memorial Excel para um projeto.
    Se memorial_id for fornecido, baixa esse. Caso contrário, usa o mais recente.
    """
    try:
        # Verifica se projeto existe
        projeto = db.query(Project).filter(Project.id == project_id).first()
        if not projeto:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
        # Busca o memorial
        if memorial_id:
            memorial = db.query(Report).filter(
                Report.id == memorial_id,
                Report.projeto_id == project_id
            ).first()
        else:
            # Pega o memorial mais recente (maior ID ou data mais recente)
            memorial = db.query(Report)\
                .filter(Report.projeto_id == project_id)\
                .order_by(Report.id.desc())\
                .first()
        
        if not memorial or not memorial.arquivo:
            raise HTTPException(status_code=404, detail="Memorial não encontrado")
        
        # Constrói caminho completo do arquivo
        backend_root = Path(__file__).parent.parent.parent
        file_path = backend_root / "uploads" / memorial.arquivo
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Arquivo de memorial não existe no servidor")
        
        # Extrai nome do arquivo para download
        filename = file_path.name
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar memorial: {str(e)}")