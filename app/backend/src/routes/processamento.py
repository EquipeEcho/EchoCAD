from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pathlib import Path
from src.database import get_session
from src.modules.ai_orchestrator import AIOrchestrator
from src.models.projeto_db import MemorialCalculo, Planta, Projeto

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

@router.post("/{project_id}/gerar-memorial")
async def gerar_memorial(
    project_id: int,
    prompt: str = Query(..., description="Prompt para geração do memorial"),
    planta_id: int = Query(None, description="ID da planta (opcional)"),
    db: Session = Depends(get_session)
):
    """
    Gera memorial em Excel para um projeto específico.
    Se planta_id for fornecido, usa DXF dessa planta. Caso contrário, usa a primeira planta do projeto.
    """
    from src.modules.core.main import run_extraction
    
    try:
        # Verifica se projeto existe
        projeto = db.query(Projeto).filter(Projeto.id == project_id).first()
        if not projeto:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
        # Determina qual planta usar
        if planta_id:
            planta = db.query(Planta).filter(
                Planta.id == planta_id,
                Planta.projeto_id == project_id
            ).first()
            if not planta:
                raise HTTPException(status_code=404, detail="Planta não encontrada neste projeto")
        else:
            # Usa primeira planta do projeto
            planta = db.query(Planta).filter(Planta.projeto_id == project_id).first()
            if not planta:
                raise HTTPException(status_code=404, detail="Nenhuma planta encontrada no projeto")
        
        # Constrói caminho do arquivo DXF
        backend_root = Path(__file__).parent.parent.parent
        dxf_path = backend_root / "uploads" / str(project_id) / planta.arquivo
        
        if not dxf_path.exists():
            raise HTTPException(status_code=404, detail=f"Arquivo DXF não encontrado: {dxf_path}")
        
        # Executa extração e gera memorial
        resultado = run_extraction(
            prompt_usuario=prompt,
            dxf_path=str(dxf_path),
            project_id=project_id,
            gerar_excel=True
        )
        
        if "erro" in resultado:
            raise HTTPException(status_code=500, detail=resultado["erro"])
        
        # Salva referência do memorial no banco de dados
        arquivo_excel = resultado.get("arquivo_excel")
        if arquivo_excel:
            memorial = MemorialCalculo(
                projeto_id=project_id,
                arquivo=arquivo_excel,
                descricao=prompt
            )
            db.add(memorial)
            db.commit()
            db.refresh(memorial)
            
            return {
                "project_id": project_id,
                "memorial_id": memorial.id,
                "arquivo": arquivo_excel,
                "descricao": "Memorial gerado com sucesso"
            }
        else:
            raise HTTPException(status_code=500, detail="Excel não foi gerado")
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao gerar memorial: {str(e)}")

