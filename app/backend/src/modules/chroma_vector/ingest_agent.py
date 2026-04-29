"""Agente de ingestao de documentos para o banco vetorial via agno.

O agno Knowledge aceita path direto e detecta PDF/DOCX automaticamente.
O AgenticChunking com Ollama divide o conteudo semanticamente antes de persistir.
Em caso de falha no chunker agentico, o Knowledge cai no RecursiveChunking.
"""

from pathlib import Path

from agno.knowledge.knowledge import Knowledge

from src.modules.chroma_vector.chunking import get_fallback_chunker
from src.modules.chroma_vector.db import get_vector_db


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def ingest_file(path: str) -> dict[str, str | int]:
    """Ingere um arquivo PDF/DOCX no banco vetorial usando agno Knowledge."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path}")

    suffix = file_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Formato nao suportado. Use apenas .pdf ou .docx")

    from agno.knowledge.reader.pdf_reader import PDFReader
    from agno.knowledge.reader.docx_reader import DocxReader

    chunker = get_fallback_chunker()
    knowledge = Knowledge(vector_db=get_vector_db())

    reader_cls = PDFReader if suffix == ".pdf" else DocxReader
    reader = reader_cls(chunking_strategy=chunker)

    knowledge.insert(
        path=str(file_path),
        reader=reader,
        metadata={"source": file_path.name, "extension": suffix},
        upsert=True,
    )

    return {
        "arquivo": file_path.name,
        "status": "ok",
    }
