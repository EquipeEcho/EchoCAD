import os
from pathlib import Path
from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.ollama import OllamaEmbedder
from pydantic import BaseModel, Field
from typing import List

# Define o caminho para o banco de dados relativo ao arquivo atual
DB_PATH = Path(__file__).parent / "tmp" / "chromadb"

knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="rules", 
        path=str(DB_PATH),
        embedder=OllamaEmbedder(id='nomic-embed-text'),
    ),
)


class LayerList(BaseModel):
    layers: List[str] = Field(
        ..., description="Lista dos nomes exatos dos layers selecionados do DXF.")


def get_selector_agent(model, tools):
    return Agent(
        name='Layer Selector Agent',
        model=model,
        # output_schema=LayerList,
        description='Seleciona os layers corretos com base no contexto, regras de negócio e na lista real do DXF.',
        markdown=True,
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "Você é um Engenheiro de Sistemas especialista em CAD/BIM.",
            "Responda exclusivamente em português brasileiro.",
            "VOCÊ DEVE OBRIGATORIAMENTE SEGUIR ESTES PASSOS:",
            "1. Consulte seu conhecimento (knowledge base) para entender as regras de nomenclatura de layers para a disciplina solicitada.",
            "2. Chame a ferramenta 'get_layers' para ver os nomes reais dos layers no arquivo DXF.",
            "3. Analise a lista retornada e identifique quais pertencem à disciplina solicitada com base nas regras encontradas.",
            "4. Use a tool 'check_exists' para validar cada um dos layers selecionados.",
            "5. Retorne como resposta a lista de nomes EXATOS dos layers validados.",
            "6. NUNCA invente nomes que não estão na lista retornada por 'get_layers'.",
        ],
        tools=tools,
    )
