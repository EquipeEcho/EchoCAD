"""Agente RAG usando agno Agent com Knowledge e Ollama.

Evita tool-calling no modelo de inferencia local para compatibilidade com
modelos Ollama que nao suportam ferramentas.
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
    """Constroi o agente de resposta sem tool-calling."""
    return Agent(
        model=Ollama(id=INFERENCE_MODEL),
        instructions=SYSTEM_PROMPT,
        markdown=False,
        search_knowledge=False,
    )


def _search_context(pergunta: str, max_results: int = 6) -> str:
    """Busca contexto no Knowledge para compor prompt RAG sem tools."""
    knowledge = Knowledge(vector_db=get_vector_db(), max_results=max_results)

    search_methods = []
    if hasattr(knowledge, "search"):
        search_methods.append(getattr(knowledge, "search"))
    if hasattr(knowledge, "query"):
        search_methods.append(getattr(knowledge, "query"))

    for method in search_methods:
        try:
            results = method(pergunta)
            if not results:
                continue

            chunks: list[str] = []
            for item in results:
                content = getattr(item, "content", None)
                if isinstance(content, str) and content.strip():
                    chunks.append(content.strip())
                elif isinstance(item, str) and item.strip():
                    chunks.append(item.strip())
                elif isinstance(item, dict):
                    text = item.get("content") or item.get("text")
                    if isinstance(text, str) and text.strip():
                        chunks.append(text.strip())

            if chunks:
                return "\n\n".join(chunks[:max_results])
        except Exception:
            continue

    return ""


def perguntar(pergunta: str) -> str:
    """Executa pergunta no agente RAG e retorna resposta textual."""
    question = (pergunta or "").strip()
    if not question:
        raise ValueError("A pergunta nao pode ser vazia")

    context = _search_context(question)
    prompt = question
    if context:
        prompt = (
            "Use o contexto abaixo para responder com precisao. "
            "Se o contexto nao contiver a resposta, diga que nao encontrou.\n\n"
            f"Contexto:\n{context}\n\n"
            f"Pergunta: {question}"
        )

    agent = _build_agent()
    response = agent.run(prompt)

    # agno retorna RunResponse com atributo content.
    content = getattr(response, "content", None)
    if isinstance(content, str) and content.strip():
        return content.strip()

    return "Nao foi possivel gerar resposta com o modelo local."
