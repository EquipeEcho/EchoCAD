from agno.agent import Agent
from agno.models.ollama import Ollama


def create_spatial_analyst_agent(tools: list):
    return Agent(
        id='spatial-analyst',
        name='Spatial Analyst',
        role='Analisa a conectividade espacial entre entidades DXF para identificar sistemas contínuos',
        description='Identifica grupos de entidades conectadas (como redes elétricas ou paredes) e calcula comprimentos totais.',
        model=Ollama(
            id='qwen2.5:3b',
            options={
                "temperature": 0.0,
                "num_ctx": 2048,
            }
        ),
        instructions=[
            '''
            Você é um especialista em topologia de projetos de engenharia.
            Sua tarefa é analisar como as entidades de um arquivo CAD estão conectadas.

            FLUXO DE TRABALHO:
            1. Use a tool `get_connectivity_graph` passando os layers relevantes.
            2. Analise os "clusters" retornados. Cada cluster representa um sistema contínuo (ex: um circuito, uma parede longa, uma tubulação).
            3. Para cada cluster, identifique o que ele representa baseado nos `identifiers` e `types`.
            4. Se houver múltiplos clusters no mesmo layer, explique se eles parecem ser partes separadas do mesmo sistema ou sistemas independentes.
            
            SAÍDA:
            - Um resumo técnico dos sistemas contínuos encontrados, seus comprimentos totais e as entidades que os compõem.
            '''
        ],
        tools=tools,
        debug_mode=True,
    )
