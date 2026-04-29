"""Chunking de documentos usando agno DocumentChunking.

DocumentChunking e o chunker padrao do PDFReader/DocxReader do agno.
Agrega conteudo por pagina e respeita o chunk_size configurado.
"""

from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.chunking.strategy import ChunkingStrategy

# Tamanho de chunk em caracteres — ~2 paginas de texto corrido.
CHUNK_SIZE = 3000


def get_fallback_chunker() -> ChunkingStrategy:
    """Retorna DocumentChunking com tamanho adequado para RAG."""
    return DocumentChunking(chunk_size=CHUNK_SIZE)
