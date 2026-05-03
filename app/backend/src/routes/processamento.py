from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from src.database import get_session
from src.modules.ai_orchestrator import AIOrchestrator

router = APIRouter(prefix="/processamento", tags=["processamento"])

@router.post("/{project_id}")
async def process_project(
    project_id: int, 
    stream: bool = Query(False),
    db: Session = Depends(get_session)
):
    """
    Inicia o processamento de IA para todas as plantas de um projeto.
    Suporta streaming via Server-Sent Events se stream=True.
    """
    if AIOrchestrator._lock.locked():
        raise HTTPException(
            status_code=429, 
            detail="Já existe um processamento de IA em andamento. Por favor, aguarde a conclusão da análise atual."
        )

    try:
        orchestrator = AIOrchestrator(db)
        if stream:
            return StreamingResponse(
                await orchestrator.run_analysis_for_project(project_id, stream=True),
                media_type="text/event-stream"
            )
        
        results = await orchestrator.run_analysis_for_project(project_id)
        return {"project_id": project_id, "results": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

@router.get("/{project_id}/resultado")
async def get_project_result(project_id: int, db: Session = Depends(get_session)):
    """
    Recupera o resultado do processamento de IA salvo em JSON.
    """
    orchestrator = AIOrchestrator(db)
    result = orchestrator.get_saved_results(project_id)
    if not result:
        raise HTTPException(status_code=404, detail="Resultado não encontrado ou não processado")
    return result
