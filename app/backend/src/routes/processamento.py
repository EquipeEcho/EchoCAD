from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_session
from src.modules.ai_orchestrator import AIOrchestrator

router = APIRouter(prefix="/processamento", tags=["processamento"])

@router.post("/{project_id}")
async def process_project(project_id: int, db: Session = Depends(get_session)):
    """
    Inicia o processamento de IA para todas as plantas de um projeto.
    """
    try:
        orchestrator = AIOrchestrator(db)
        results = orchestrator.run_analysis_for_project(project_id)
        return {"project_id": project_id, "results": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
