"""Processador para extrair texto de arquivos DOCX e PDF."""

from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text_from_docx(file_path: str) -> str:
    """Extrai todo o texto de um arquivo DOCX.

    Args:
        file_path: Caminho para o arquivo DOCX.

    Returns:
        str: Texto completo extraído do documento.

    Raises:
        Exception: Se houver erro ao ler o arquivo.
    """
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip() if text else ""
    except Exception as e:
        raise Exception(f"Erro ao ler DOCX: {str(e)}")


def extract_text_from_pdf(file_path: str) -> str:
    """Extrai todo o texto de um arquivo PDF.

    Args:
        file_path: Caminho para o arquivo PDF.

    Returns:
        str: Texto completo extraído do documento.

    Raises:
        Exception: Se houver erro ao ler o arquivo.
    """
    try:
        reader = PdfReader(file_path)
        text_parts = []

        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text:
                text_parts.append(f"[Página {page_num}]\n{text}")

        return "\n".join(text_parts).strip() if text_parts else ""
    except Exception as e:
        raise Exception(f"Erro ao ler PDF: {str(e)}")


def extract_text_from_file(file_path: str) -> str:
    """Detecta o tipo de arquivo e extrai texto automaticamente.

    Args:
        file_path: Caminho para o arquivo (DOCX ou PDF).

    Returns:
        str: Texto extraído do documento.

    Raises:
        ValueError: Se o tipo de arquivo não é suportado.
        Exception: Se houver erro ao processar o arquivo.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".docx":
        return extract_text_from_docx(file_path)
    elif suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {suffix}. Use .docx ou .pdf")
