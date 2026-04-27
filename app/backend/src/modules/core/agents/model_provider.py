from agno.models.groq import Groq
from agno.models.ollama import Ollama
from config import settings

fast_model = Groq(
    id="groq/compound",
    # id="llama-3.1-8b-instant",
    api_key=settings.groq_api_key
)

strong_model = Groq(
    id="llama-3.3-70b-versatile",
    api_key=settings.groq_api_key
)

privacity_model = Ollama(
    id='qwen2.5'
)
