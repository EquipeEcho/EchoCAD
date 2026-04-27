from agno.agent import Agent
from modules.core.agents.model_provider import fast_model
from pydantic import BaseModel

class Response (BaseModel):
    layers: dict[int, str]

def get_selector_agent(tools):
    return Agent(
        name='Layer Selector Agent',
        model=fast_model,
        output_schema=Response,
        description='Seleciona os layers úteis com base no contexto estruturado e na lista real do DXF.',
        instructions=[
            "Você é um Engenheiro de Sistemas especialista em CAD/BIM.",
            "Sua tarefa é analisar os layers recebidos, inferir quais fazem parte do contexto.",
            "Ao interir os layers corretos, devolver no formato apenas os layers inferidos",
            "REGRAS:",
            "1. Você DEVE chamar 'get_layers' para ver quais camadas existem de verdade.",
            "2. Selecione apenas os números dos layers que tenham impacto direto na execução do objetivo (eletrica, spda, etc).",
            "3. O retorno deve ser feito com o resultado da tool 'get_set_layers'",
        ],
        tools=tools,
    )
