"""Conexao com ChromaDB via agno — banco vetorial persistente com embeddings Ollama."""

from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.vectordb.chroma import ChromaDb

# Caminho de persistencia local do ChromaDB.
CHROMA_PATH = "./chroma_db"

# Nome da colecao principal.
COLLECTION_NAME = "normas"

# Modelo de embedding local via Ollama.
# Usa nomic-embed-text (128 dims) por ser leve e especifico para embeddings.
# Ajuste o id e dimensions se preferir outro modelo disponivel no seu Ollama.
EMBED_MODEL = "nomic-embed-text"
EMBED_DIMENSIONS = 768


def get_vector_db() -> ChromaDb:
    """Retorna instancia configurada do ChromaDb com embedder Ollama."""
    embedder = OllamaEmbedder(id=EMBED_MODEL, dimensions=EMBED_DIMENSIONS)
    return ChromaDb(
        collection=COLLECTION_NAME,
        path=CHROMA_PATH,
        persistent_client=True,
        embedder=embedder,
    )
