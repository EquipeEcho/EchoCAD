from agno.agent import Agent
from pydantic import BaseModel, Field
from typing import List

class LayerList(BaseModel):
    layers: List[str] = Field(..., description="Lista dos nomes exatos dos layers selecionados do DXF.")

def get_selector_agent(model, tools):
    return Agent(
        name='Layer Selector Agent',
        model=model,
        description='Seleciona os layers corretos com base no contexto e na lista real do DXF.',
        instructions=[
            "Você é um Engenheiro de Sistemas especialista em CAD/BIM.",
            "VOCÊ DEVE OBRIGATORIAMENTE SEGUIR ESTES PASSOS:",
            "1. Chame a ferramenta 'get_layers' para ver os nomes reais dos layers no arquivo.",
            "2. Analise a lista retornada e identifique quais pertencem à disciplina solicitada (ex: Elétrica).",
            "3. Se o contexto for 'Elétrica', procure por layers que comecem com 'ELE-' ou contenham 'ELET'.",
            "4. Retorne a lista de nomes EXATOS dos layers selecionados.",
            "NUNCA invente nomes que não estão na lista de 'get_layers'.",
        ],
        tools=tools,
    )
