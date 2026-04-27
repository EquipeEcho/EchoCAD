"""Aplicacao principal do sistema RAG com agno, ChromaDB e Ollama."""

import argparse
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from src.modules.chroma_vector.ingest_agent import ingest_file
from src.modules.chroma_vector.rag_agent import perguntar

app = FastAPI(
    title="EchoCAD RAG Local — agno",
    description="RAG agentico com agno Knowledge + ChromaDB + Ollama llama3.",
    version="2.0.0",
)


@app.get("/")
def health_check() -> dict[str, str]:
    """Status da API."""
    return {"status": "ok", "service": "echocad-rag-agno"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict[str, str | int]:
    """Recebe PDF/DOCX, ingere no ChromaDB via agno Knowledge."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo sem nome")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Apenas .pdf e .docx sao suportados")

    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        result = ingest_file(temp_path)
        result["arquivo"] = file.filename
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha na ingestao: {exc}") from exc
    finally:
        if temp_path and Path(temp_path).exists():
            Path(temp_path).unlink(missing_ok=True)


@app.get("/perguntar")
def endpoint_perguntar(
    pergunta_usuario: str = Query(..., alias="pergunta", min_length=1),
) -> dict[str, str]:
    """Executa pergunta no agente RAG agentico e retorna resposta."""
    try:
        resposta = perguntar(pergunta_usuario)
        return {"resposta": resposta}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha ao responder: {exc}") from exc


def _run_cli_example(files: list[str], question: str | None) -> None:
    """Uso local sem API."""
    for file_path in files:
        result = ingest_file(file_path)
        print(f"Ingestao concluida: {result}")

    if question:
        answer = perguntar(question)
        print("\nPergunta:", question)
        print("Resposta:", answer)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sistema RAG local — agno + ChromaDB + Ollama")
    parser.add_argument("--ingest", nargs="*", default=[], help="Arquivos PDF/DOCX para ingestao")
    parser.add_argument("--ask", default=None, help="Pergunta para o agente RAG")
    parser.add_argument("--serve", action="store_true", help="Inicia a API FastAPI")
    return parser


if __name__ == "__main__":
    import uvicorn

    args = _build_parser().parse_args()

    if args.serve:
        uvicorn.run(app, host="0.0.0.0", port=8010)
    else:
        _run_cli_example(files=args.ingest, question=args.ask)
