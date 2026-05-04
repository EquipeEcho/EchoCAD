from agno.agent import Agent
from src.aiconf import medium_model


def create_classificator_agent(tools: list):
    return Agent(
        id='agent-layer-select',
        name='Agent Layer Select',
        role='Selecione os layer relevantes associados a uma disciplina de engenharia fornecida.',
        description='Filtra a lista real de layers de um arquivo DXF usando a disciplina como keyword.',
        model=medium_model,
        instructions=[
            '''
            Você é um especialista em estruturação de layers CAD (AIA CAD Standards).
            Sua missão é selecionar APENAS os layers que pertencem EXCLUSIVAMENTE à disciplina solicitada.

            REGRAS DE SELEÇÃO:
            - Alvenaria: Apenas camadas de paredes e estruturas (Ex: arq-alvenaria). Não inclua esquadrias ou mobiliário.
            - Elétrica: Camadas de fiação, tomadas, iluminação e força (Ex: ele-*, ilum-*).
            - Hidráulica: Camadas de água fria, quente, esgoto, dreno e pluvial (Ex: hid-*).
            - Rede/Dados: Camadas de lógica e comunicação (Ex: net-*, dados-*).

            FERRAMENTA:
            1. Use `get_layers` para ver a lista real.
            2. Compare o contexto com a lista.
            
            SAÍDA:
            Retorne APENAS o JSON com a lista de nomes. Ex: ["layer1", "layer2"].
            Não adicione texto explicativo.
            '''
        ],
        tools=tools,
        use_json_mode=True,
        markdown=False,
    )
