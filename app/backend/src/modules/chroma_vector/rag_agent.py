"""Agente RAG usando agno Agent com Knowledge e Ollama.

O agno Agent com search_knowledge=True implementa Agentic RAG:
o proprio agente decide quando buscar no banco vetorial antes de responder.
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import Ollama

from src.modules.chroma_vector.db import get_vector_db

# System prompt restringindo respostas ao contexto dos documentos.
SYSTEM_PROMPT = (
    "Voce e um assistente especialista nos documentos carregados. "
    "Responda APENAS com base nas informacoes encontradas nos documentos. "
    "Se a informacao nao estiver nos documentos, diga explicitamente que nao encontrou. "
    "Seja objetivo e cite a fonte quando possivel."
)

# Modelo local usado para inferencia.
INFERENCE_MODEL = "llama3"


def _build_agent() -> Agent:
    """Constroi o agente RAG com knowledge base e modelo Ollama."""
    knowledge = Knowledge(
        vector_db=get_vector_db(),
        max_results=3,
    )
    return Agent(
        model=Ollama(id=INFERENCE_MODEL),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=SYSTEM_PROMPT,
        markdown=False,
    )


def perguntar(pergunta: str) -> str:
    """Executa pergunta no agente RAG e retorna resposta textual."""
    question = (pergunta or "").strip()
    if not question:
        raise ValueError("A pergunta nao pode ser vazia")

    agent = _build_agent()
    response = agent.run(question)

    # agno retorna RunResponse com atributo content.
    content = getattr(response, "content", None)
    if isinstance(content, str) and content.strip():
        return content.strip()

    return "Nao foi possivel gerar resposta com o modelo local."
