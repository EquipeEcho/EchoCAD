"""API FastAPI para leitura de dados da coleção vetorial 'normas'."""

import tempfile
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Query, UploadFile
from pydantic import BaseModel

from src.modules.chroma_vector.db import get_collection
from src.modules.chroma_vector.document_processor import extract_text_from_file

app = FastAPI(
    title="API de Normas com ChromaDB",
    description="API simples para leitura e busca por similaridade em um banco vetorial local.",
    version="1.0.0",
)


class NormaCreate(BaseModel):
    """Modelo para criar uma norma manualmente."""

    id: str
    document: str
    metadata: dict[str, str]


def _format_all_documents(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Converte retorno do ChromaDB em uma lista de itens estruturados.

    Args:
        raw_data: Resultado bruto retornado por collection.get(...).

    Returns:
        list[dict[str, Any]]: Lista com id, documento e metadados.
    """
    ids = raw_data.get("ids", []) or []
    documents = raw_data.get("documents", []) or []
    metadatas = raw_data.get("metadatas", []) or []

    items: list[dict[str, Any]] = []
    for idx, doc_id in enumerate(ids):
        items.append(
            {
                "id": doc_id,
                "document": documents[idx] if idx < len(documents) else None,
                "metadata": metadatas[idx] if idx < len(metadatas) else None,
            }
        )

    return items


def _format_query_results(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Converte resultado de query em itens legíveis para a API.

    O ChromaDB retorna listas aninhadas por causa do suporte a múltiplas
    consultas no mesmo request. Como usamos apenas uma query por vez,
    pegamos o índice 0 de cada lista.
    """
    ids = (raw_data.get("ids") or [[]])[0]
    documents = (raw_data.get("documents") or [[]])[0]
    metadatas = (raw_data.get("metadatas") or [[]])[0]
    distances = (raw_data.get("distances") or [[]])[0]

    items: list[dict[str, Any]] = []
    for idx, doc_id in enumerate(ids):
        items.append(
            {
                "id": doc_id,
                "document": documents[idx] if idx < len(documents) else None,
                "metadata": metadatas[idx] if idx < len(metadatas) else None,
                "distance": distances[idx] if idx < len(distances) else None,
            }
        )

    return items


@app.get("/normas")
def list_normas() -> dict[str, Any]:
    """Retorna todos os documentos armazenados na coleção 'normas'."""
    collection = get_collection()

    # Inclui documentos e metadados no retorno.
    raw_data = collection.get(include=["documents", "metadatas"])
    items = _format_all_documents(raw_data)

    return {
        "collection": "normas",
        "total": len(items),
        "items": items,
    }


@app.get("/buscar")
def buscar_normas(query: str = Query(..., min_length=1)) -> dict[str, Any]:
    """Busca os 5 documentos mais similares ao texto informado."""
    collection = get_collection()

    # Busca semântica com top 5 resultados mais próximos.
    raw_data = collection.query(
        query_texts=[query],
        n_results=5,
        include=["documents", "metadatas", "distances"],
    )
    items = _format_query_results(raw_data)

    return {
        "query": query,
        "total": len(items),
        "results": items,
    }


@app.get("/")
def health_check() -> dict[str, str]:
    """Endpoint simples para confirmar que a API está ativa."""
    return {"status": "ok", "message": "API no ar."}


@app.post("/normas")
def criar_norma(norma: NormaCreate) -> dict[str, str]:
    """Insere uma norma manualmente na coleção."""
    collection = get_collection()

    collection.add(
        ids=[norma.id],
        documents=[norma.document],
        metadatas=[norma.metadata],
    )

    return {"message": "Norma inserida com sucesso", "id": norma.id}


@app.post("/upload-documento")
async def upload_documento(file: UploadFile = File(...)) -> dict[str, Any]:
    """Faz upload de um arquivo DOCX ou PDF e adiciona à coleção.

    Extrai o texto completo do documento e o adiciona como uma norma.
    """
    # Valida o tipo de arquivo
    if file.filename is None:
        return {"error": "Arquivo sem nome"}

    suffix = Path(file.filename).suffix.lower()
    if suffix not in [".docx", ".pdf"]:
        return {"error": "Apenas arquivos .docx e .pdf são suportados"}

    try:
        # Salva temporariamente o arquivo recebido
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Extrai o texto do arquivo
        extracted_text = extract_text_from_file(tmp_path)

        if not extracted_text:
            return {"error": "Nenhum texto foi extraído do documento"}

        # Gera um ID único para a norma
        norma_id = f"norma-{uuid.uuid4().hex[:8]}"

        # Adiciona à coleção
        collection = get_collection()
        collection.add(
            ids=[norma_id],
            documents=[extracted_text],
            metadatas=[
                {
                    "filename": file.filename,
                    "file_type": suffix[1:].upper(),
                }
            ],
        )

        # Remove arquivo temporário
        Path(tmp_path).unlink()

        return {
            "message": "Documento processado e adicionado com sucesso",
            "id": norma_id,
            "filename": file.filename,
            "text_length": len(extracted_text),
        }

    except Exception as e:
        return {"error": f"Erro ao processar arquivo: {str(e)}"}
