from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

# Configuração do Knowledge (mesma do seu código)
knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="rules",
        path="tmp/chromadb",
        embedder=OllamaEmbedder(id='openhermes'),
        persistent_client=True
    )
)


def ingest_rules():
    """
    Executa a inserção das regras de negócio no Knowledge Base.
    """
    rules = [
        "Para a disciplina de Elétrica, considere layers com prefixos: ELE-, -ELE, ELT, ELET.",
        "Sistemas de proteção como SPDA, Aterramento e Malha de Terra pertencem à Elétrica.",
        "Símbolos de quadros e diagramas elétricos também devem ser selecionados.",
        "Nomes como 'Circuitos', 'Fiação' e 'Iluminação' são sempre da disciplina elétrica."
    ]

    # Adiciona as regras ao banco vetorial
    # O Agno/Chroma cuida para não duplicar se você gerenciar os IDs ou limpar antes
    knowledge.insert(
        name='rules',
        text_content="\n".join(rules),
    )
    print("Regras de engenharia inseridas com sucesso!")


# Execute isso apenas uma vez ou via CLI
ingest_rules()
