"""
Exceções customizadas para o sistema de processamento de IA.
Utilisadas para comunicar erros claros ao frontend via API.
"""


class AIProviderException(Exception):
    """Base para erros de provedor de IA"""
    pass


class NoGroqTokenException(AIProviderException):
    """Sem token Groq disponível (nem no .env nem no perfil do usuário)"""
    pass


class OllamaUnavailableException(AIProviderException):
    """Ollama não está respondendo na URL configurada"""
    pass


class GroqQuotaExceededException(AIProviderException):
    """Limite de uso mensal do Groq foi atingido"""
    pass


class NoValidProviderException(AIProviderException):
    """Nenhum provedor de IA está disponível"""
    pass
