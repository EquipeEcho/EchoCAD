from agno.models.groq import Groq
from agno.models.ollama import Ollama
from config import settings

# Groq Models (Cloud)
fast_model = Groq(
    id="llama-3.1-8b-instant",
    api_key=settings.groq_api_key
)

strong_model = Groq(
    id="llama-3.3-70b-versatile",
    api_key=settings.groq_api_key
)

# Ollama Models (Local Deployment)
def get_ollama_model(model_name='qwen2.5'):
    """
    Returns an Ollama model instance. 
    Supports 'qwen2.5' or 'qwen3' (as requested for deploy).
    """
    return Ollama(id=model_name)

# Default privacy model
privacity_model = get_ollama_model('qwen2.5')
