import argparse
from pathlib import Path

from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb


CHROMA_PATH = Path(__file__).parent / "tmp" / "chromadb"
COLLECTION_NAME = "docs"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIMENSIONS = 768


def get_vector_db(chroma_path: Path) -> ChromaDb:
    return ChromaDb(
        collection=COLLECTION_NAME,
        path=str(chroma_path),
        persistent_client=True,
        embedder=OllamaEmbedder(id=EMBED_MODEL, dimensions=EMBED_DIMENSIONS),
    )


def query_chroma(prompt: str, chroma_path: Path, max_results: int = 5):
    knowledge = Knowledge(vector_db=get_vector_db(chroma_path), max_results=max_results)

    if hasattr(knowledge, "search"):
        try:
            return knowledge.search(prompt)
        except Exception:
            pass

    if hasattr(knowledge, "query"):
        return knowledge.query(prompt)

    raise RuntimeError("Nenhum metodo de busca disponivel em Knowledge")


def format_result(item, index: int) -> str:
    if isinstance(item, str):
        text = item
    elif isinstance(item, dict):
        text = item.get("content") or item.get("text") or str(item)
    else:
        text = getattr(item, "content", None) or getattr(item, "text", None) or str(item)

    text = text.strip() if isinstance(text, str) else str(text)
    return f"Result {index}:\n{text}\n{'-' * 80}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consulta direta ao ChromaDB sem usar agentes."
    )
    parser.add_argument("query", help="Termo ou frase para buscar na base de conhecimento.")
    parser.add_argument("-n", "--num", type=int, default=5, help="Número máximo de resultados a retornar.")
    parser.add_argument("--chroma-path", default=str(CHROMA_PATH), help="Caminho do diretório ChromaDB.")
    args = parser.parse_args()

    chroma_path = Path(args.chroma_path)
    results = query_chroma(args.query, chroma_path, max_results=args.num)

    if not results:
        print("Nenhum resultado encontrado.")
        return

    print(f"Mostrando até {args.num} resultados para: {args.query}" )
    print("=" * 80)
    for i, item in enumerate(results, start=1):
        print(format_result(item, i))


if __name__ == "__main__":
    main()
