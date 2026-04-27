"""Chunking inteligente usando agno.

Usa AgenticChunking com Ollama (llama3) para divisao semantica.
Fallback automatico para RecursiveChunking em caso de falha do modelo.
"""

from agno.knowledge.chunking.agentic import AgenticChunking
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.knowledge.chunking.strategy import ChunkingStrategy
from agno.models.ollama import Ollama

# Tamanho maximo de chunk em caracteres para o fallback recursivo.
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150

# Modelo local usado para chunking semantico.
CHUNKING_MODEL = "llama3"


def get_agentic_chunker() -> ChunkingStrategy:
    """Retorna AgenticChunking com Ollama como estrategia principal."""
    return AgenticChunking(
        model=Ollama(id=CHUNKING_MODEL),
        max_chunk_size=CHUNK_SIZE,
    )


def get_fallback_chunker() -> ChunkingStrategy:
    """Retorna RecursiveChunking como fallback deterministico."""
    return RecursiveChunking(chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
