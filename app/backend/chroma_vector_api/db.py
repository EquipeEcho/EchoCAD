"""Configuração e acesso ao ChromaDB.

Este módulo centraliza a conexão com o banco vetorial e disponibiliza
funções utilitárias para obter a coleção usada pela API.
"""

from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

# Diretório local onde o ChromaDB salva os dados persistentemente.
CHROMA_PATH = Path(__file__).parent / "chroma_db"

# Nome da coleção principal usada neste projeto.
COLLECTION_NAME = "normas"


def get_collection() -> Collection:
    """Retorna a coleção 'normas', criando-a se necessário.

    Returns:
        Collection: Instância da coleção conectada ao banco vetorial local.
    """
    # Garante que a pasta de persistência exista antes de iniciar o client.
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    # Cliente com persistência local em disco.
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    # Busca a coleção existente ou cria uma nova com o nome definido.
    return client.get_or_create_collection(name=COLLECTION_NAME)
