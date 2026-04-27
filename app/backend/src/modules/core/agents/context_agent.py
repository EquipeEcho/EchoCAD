from agno.agent import Agent
from pydantic import BaseModel, Field
from modules.core.agents.model_provider import fast_model, privacity_model


class Response(BaseModel):
    objective: str = Field(..., description='Objetivo principal da obra')
    cause: str = Field(..., description='Causa ou razão da realização da obra')
    description: str = Field(...,
                             description='Descrição resumida do que será feito')
    keywords: str = Field(...,
                          description='Palavras chave dos nomes dos elementos')
    locals: str = Field(..., description='Localização ou endereço da obra')


context_agent = Agent(
    name='ContextAgent',
    model=fast_model,
    output_schema=Response,
    description='Faz a triagem de informações sobre a natureza do projeto.',
    instructions=[
        "Você é um engenheiro especialista em triagem de projetos e análise de editais.",
        "Sua tarefa é converter textos brutos de objetivos e justificativas em dados estruturados.",
        "Cada campo deve conter informações relacionadas ao campo apenas.",
        "Cada resposta deve ser objetiva e resumida.",
        "Não inclua nenhuma saudação ou textos desnecessários."
    ],
)
