"""
Configuração centralizada de modelos de IA para o EchoCAD.

Define 3 níveis de modelos:
- quick: Modelo rápido para tarefas simples (1.5B)
- medium: Modelo intermediário para tarefas normais (3B)
- high: Modelo poderoso para tarefas complexas (7B)

Suporta switch entre Groq e Ollama para testes rápidos.
"""

import os
from typing import Literal

# ============================================================================
# CONFIGURAÇÃO GLOBAL: Escolha o provider de IA
# ============================================================================

AI_PROVIDER: Literal["groq", "ollama"] = os.getenv("AI_PROVIDER", "groq").lower()
"""
Defina para:
- "groq": Usa Groq Cloud API (mais rápido em testes, requer chave de API)
- "ollama": Usa Ollama local (mais lento, sem custo)

Pode ser alterado via variável de ambiente: AI_PROVIDER=groq ou AI_PROVIDER=ollama
"""

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
"""Chave de API do Groq (necessária se AI_PROVIDER=groq)"""

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
"""URL base do servidor Ollama (necessária se AI_PROVIDER=ollama)"""

# ============================================================================
# MODELOS DISPONÍVEIS
# ============================================================================

if AI_PROVIDER == "groq":
    # Groq - https://console.groq.com/docs/speech-text
    from agno.models.groq import Groq
    
    # Modelo RÁPIDO (quick) - Ideal para extrações simples e respostas rápidas
    quick_model = Groq(
        id="mixtral-8x7b-32768",  # Modelo rápido no Groq
        name="quick_model",
    )
    
    # Modelo MÉDIO (medium) - Ideal para processamento balanceado
    medium_model = Groq(
        id="mixtral-8x7b-32768",  # Mesmo modelo, mas pode ser ajustado
        name="medium_model",
    )
    
    # Modelo ALTO (high) - Ideal para tarefas complexas e análises detalhadas
    high_model = Groq(
        id="mixtral-8x7b-32768",  # Melhor modelo do Groq
        name="high_model",
    )

elif AI_PROVIDER == "ollama":
    # Ollama - Local inference
    from agno.models.ollama import Ollama
    
    # Modelo RÁPIDO (quick) - qwen2.5:1.5b
    quick_model = Ollama(
        id="qwen2.5:1.5b",
        name="quick_model",
        base_url=OLLAMA_BASE_URL,
    )
    
    # Modelo MÉDIO (medium) - qwen2.5:3b
    medium_model = Ollama(
        id="qwen2.5:3b",
        name="medium_model",
        base_url=OLLAMA_BASE_URL,
    )
    
    # Modelo ALTO (high) - qwen2.5:7b
    high_model = Ollama(
        id="qwen2.5:7b",
        name="high_model",
        base_url=OLLAMA_BASE_URL,
    )

else:
    raise ValueError(
        f"AI_PROVIDER inválido: {AI_PROVIDER}. Use 'groq' ou 'ollama'"
    )

# ============================================================================
# EXPORTAÇÕES PRINCIPAIS
# ============================================================================

__all__ = [
    "AI_PROVIDER",
    "GROQ_API_KEY",
    "OLLAMA_BASE_URL",
    "quick_model",
    "medium_model",
    "high_model",
]

# ============================================================================
# INFORMAÇÕES DE DEBUG
# ============================================================================

if __name__ == "__main__":
    print(f"✓ AI Provider: {AI_PROVIDER}")
    print(f"✓ Quick Model: {quick_model.id if hasattr(quick_model, 'id') else quick_model}")
    print(f"✓ Medium Model: {medium_model.id if hasattr(medium_model, 'id') else medium_model}")
    print(f"✓ High Model: {high_model.id if hasattr(high_model, 'id') else high_model}")
