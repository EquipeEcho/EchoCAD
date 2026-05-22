import os
from pathlib import Path

from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.docx_reader import DocxReader
from agno.vectordb.chroma import ChromaDb


def main() -> None:
    root = Path(__file__).parent

    knowledge = Knowledge(
        vector_db=ChromaDb(
            collection="docs",
            path="tmp/chromadb",
            persistent_client=True,
            embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768),
        ),
        max_results=3,
    )

    reader = DocxReader(chunking_strategy=DocumentChunking(chunk_size=768, overlap=80))

    knowledge.insert(
        path=root / "spda.docx",
        reader=reader,
        metadata={"assunto": "documento objetivo"},
    )

    agent = Agent(
        model=Groq(
            id="llama-3.1-8b-instant",
            api_key=os.getenv(
                "GROQ_API_KEY",
                "",
            ),
        ),
        knowledge=knowledge,
        search_knowledge=True,
    )

    agent.print_response(
        "Qual é o objetivo do projeto? consulte o conhecimento pra averiguar"
    )


if __name__ == "__main__":
    main()
