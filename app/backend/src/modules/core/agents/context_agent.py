from agno.agent import Agent
from pydantic import BaseModel, Field

class ContextResponse(BaseModel):
    objective: str = Field(..., description='Objetivo da obra')
    cause: str = Field(..., description='Causa ou razão da realização da obra')
    description: str = Field(..., description='Descrição do que será feito')
    keywords: str = Field(..., description='Elementos comuns de obras')
    locals: str = Field(..., description='Localização ou endereço da obra')

def get_context_agent(model):
    return Agent(
        name='ContextAgent',
        model=model,
        description='Faz a triagem de informações sobre a natureza do projeto.',
        instructions=[
            "Você é um engenheiro especialista em triagem de projetos e análise de editais.",
            "Sua tarefa é converter textos brutos de objetivos e justificativas em dados estruturados.",
            "Retorne a resposta com os campos: objetivo, causa, descrição, palavras-chave e localização.",
            "Cada resposta deve ser objetiva e resumida."
        ],
    )

