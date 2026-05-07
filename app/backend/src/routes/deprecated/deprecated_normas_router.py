"""Exemplo de integração do agente RAG de normas com FastAPI.

Este arquivo serve como referência para como integrar o módulo knowledge
com as rotas do FastAPI do EchoCAD.

Arquivo recomendado: src/routes/normas_router.py
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from results.knowledge import query_normas
from results.knowledge.normas_rag_agent import query_normas_com_fontes
from results.knowledge.normas_ingestor import ingest_norma_file, ingest_normas_batch


router = APIRouter(prefix="/api/normas", tags=["normas"])


# ============================================================================
# MODELOS
# ============================================================================

class NormaConsultaRequest(BaseModel):
    """Requisição de consulta em normas"""
    pergunta: str


class NormaConsultaResponse(BaseModel):
    """Resposta de consulta em normas"""
    pergunta: str
    resposta: str
    fontes: int | None = None
    contexto_disponivel: bool


class NormaIngestResponse(BaseModel):
    """Resposta de ingestão de norma"""
    status: str
    arquivo: str
    norma_id: str
    documentos: int


class NormaIngestBatchResponse(BaseModel):
    """Resposta de ingestão em batch"""
    total: int
    sucesso: int
    erro: int


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/consultar", response_model=NormaConsultaResponse)
async def consultar_normas(request: NormaConsultaRequest):
    """Consulta normas técnicas com RAG.
    
    Usa embeddings semânticos para recuperar trechos relevantes
    e responde usando modelo LLM local.
    
    Args:
        pergunta: Pergunta sobre normas técnicas
        
    Returns:
        NormaConsultaResponse com resposta e metadata
        
    Example:
        POST /api/normas/consultar
        {
            "pergunta": "Como dimensionar uma viga de concreto armado?"
        }
    """
    if not request.pergunta or not request.pergunta.strip():
        raise HTTPException(status_code=400, detail="Pergunta não pode ser vazia")
    
    try:
        resposta = query_normas(request.pergunta)
        
        return NormaConsultaResponse(
            pergunta=request.pergunta,
            resposta=resposta,
            contexto_disponivel=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consultar-com-fontes", response_model=NormaConsultaResponse)
async def consultar_normas_com_fontes(request: NormaConsultaRequest):
    """Consulta normas e retorna informações sobre fontes.
    
    Útil para auditoria e verificação das normas consultadas.
    
    Args:
        pergunta: Pergunta sobre normas técnicas
        
    Returns:
        NormaConsultaResponse com resposta e número de fontes
    """
    if not request.pergunta or not request.pergunta.strip():
        raise HTTPException(status_code=400, detail="Pergunta não pode ser vazia")
    
    try:
        resultado = query_normas_com_fontes(request.pergunta)
        
        return NormaConsultaResponse(
            pergunta=resultado["pergunta"],
            resposta=resultado["resposta"],
            fontes=resultado["fontes_consultadas"],
            contexto_disponivel=resultado["contexto_disponível"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest-arquivo", response_model=NormaIngestResponse)
async def ingest_norma_arquivo(
    file_path: str,
    norma_id: str | None = None,
    background_tasks: BackgroundTasks = None,
):
    """Ingere um arquivo de norma PDF no banco vetorial.
    
    Processa o PDF, divide em chunks semânticos e armazena
    embeddings no ChromaDB.
    
    Args:
        file_path: Caminho para arquivo PDF
        norma_id: Identificador da norma (ex: "NBR 6118")
        
    Returns:
        NormaIngestResponse com status da ingestão
        
    Example:
        POST /api/normas/ingest-arquivo?file_path=/uploads/nbr6118.pdf&norma_id=NBR%206118
    """
    try:
        resultado = ingest_norma_file(file_path, norma_id=norma_id)
        
        if resultado["status"] != "sucesso":
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao ingestar norma: {resultado.get('erro')}",
            )
        
        return NormaIngestResponse(
            status="sucesso",
            arquivo=resultado["arquivo"],
            norma_id=resultado["norma_id"],
            documentos=resultado["documentos_processados"],
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest-lote", response_model=NormaIngestBatchResponse)
async def ingest_normas_lote(
    diretorio: str,
    background_tasks: BackgroundTasks = None,
):
    """Ingere múltiplas normas de um diretório.
    
    Processa todos os PDFs em um diretório para o banco vetorial.
    Operação pode demorar dependendo do número de normas.
    
    Args:
        diretorio: Caminho para diretório com PDFs
        
    Returns:
        NormaIngestBatchResponse com estatísticas
        
    Example:
        POST /api/normas/ingest-lote?diretorio=/uploads/normas/
    """
    try:
        resultado = ingest_normas_batch(diretorio)
        
        return NormaIngestBatchResponse(
            total=resultado["total"],
            sucesso=resultado["sucesso"],
            erro=resultado["erro"],
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Diretório não encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def status_normas():
    """Retorna status do módulo de normas.
    
    Returns:
        dict com informações sobre o banco de normas
        
    Example:
        GET /api/normas/status
    """
    return {
        "modulo": "knowledge-rag",
        "versao": "1.0.0",
        "banco_vetorial": "chromadb",
        "modelo_embedding": "nomic-embed-text",
        "modelo_inferencia": "qwen2.5:7b",
        "status": "operacional",
    }


# ============================================================================
# HEALTHCHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Verifica saúde do módulo de normas.
    
    Returns:
        dict com status e dados do sistema
    """
    try:
        # Testa conexão com bank
        from results.knowledge.db import get_normas_vector_db
        vector_db = get_normas_vector_db()
        
        # Testa modelo
        resposta = query_normas("Teste de conexão")
        
        return {
            "status": "healthy",
            "banco_vetorial": "ok",
            "modelo_inferencia": "ok",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "erro": str(e),
        }
