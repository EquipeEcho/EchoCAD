from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.reader.docx_reader import DocxReader
from agno.knowledge.reader.docling_reader import DoclingReader
from agno.vectordb.chroma import ChromaDb
from pathlib import Path

# Create a knowledge base
knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        # persistent_client=True,
        embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768),
        # max_results=3,
    ),
    max_results=3
)

root = Path(__file__).parent
# Load content
knowledge.insert(
    path=(root / 'pc.pdf'),
    reader=PDFReader(
        chunking_strategy=FixedSizeChunking(
            chunk_size=500,
            overlap=50
        )
    ),
    metadata={'assunto':'informática'}
)

knowledge.insert(
    path=(root / 'car.pdf'),
    reader=PDFReader(
        chunking_strategy=FixedSizeChunking(
            chunk_size=500,
            overlap=50
        )
    ),
    metadata={'assunto': 'automotivo'}
)

knowledge.insert(
    path=(root / 'umb.docx'),
    reader=DocxReader(
        chunking_strategy=FixedSizeChunking(
            chunk_size=500,
            overlap=50
        )
    ),
    metadata={'assunto': 'espiritualidade'}
)


# Create an agent that searches the knowledge base
agent = Agent(
    model=Groq(
        id="llama-3.1-8b-instant",
        api_key=""
    ),
    knowledge=knowledge,
    search_knowledge=True,
    # enable_agentic_knowledge_filters=True
)
agent.print_response('Qual orixá é responsável pela riquisa material?')