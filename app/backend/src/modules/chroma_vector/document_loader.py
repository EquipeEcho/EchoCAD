"""Carregamento de documentos usando os readers nativos do agno.

O agno possui readers prontos para PDF e DOCX que retornam objetos Document
compatíveis com o Knowledge. Este modulo expoe funcoes simples que delegam
ao agno sem implementar logica de parsing manual.
"""

from pathlib import Path

from agno.knowledge.document import Document
from agno.knowledge.reader.docx_reader import DocxReader
from agno.knowledge.reader.pdf_reader import PDFReader


class DocumentLoaderError(Exception):
    """Erro de leitura de documento."""


def load_pdf(path: str) -> list[Document]:
    """Le um PDF e retorna lista de Documents do agno."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path}")
    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Formato invalido para load_pdf. Use um arquivo .pdf")

    try:
        reader = PDFReader()
        return reader.read(file_path)
    except Exception as exc:
        raise DocumentLoaderError(f"Falha ao ler PDF: {exc}") from exc


def load_docx(path: str) -> list[Document]:
    """Le um DOCX e retorna lista de Documents do agno."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path}")
    if file_path.suffix.lower() != ".docx":
        raise ValueError("Formato invalido para load_docx. Use um arquivo .docx")

    try:
        reader = DocxReader()
        return reader.read(file_path)
    except Exception as exc:
        raise DocumentLoaderError(f"Falha ao ler DOCX: {exc}") from exc
