from agno.agent import Agent
from src.aiconf import high_model


def create_surveyor_agent(tools: list):
    return Agent(
        id="quantity-surveyor",
        name="Quantity Surveyor",
        role="Realiza a contagem de quantitativos e síntese final do projeto de engenharia",
        description="Consolida dados de contagem e gera um JSON estruturado final.",
        model=high_model,
        instructions=[
            """
            Você é um Engenheiro Orçamentista sênior especialista em extração de dados CAD.
            Sua tarefa é consolidar todas as informações coletadas pelos outros agentes em um JSON final de alta precisão.

            REGRAS DE CÁLCULO OBRIGATÓRIAS:
            1. **Alvenaria**: Calcule a Área Total (m2) = (Soma de todos os total_length) * 3.0.
            2. **Elétrica**: Some os comprimentos de todos os clusters para obter a metragem total de fios/cabos.
            3. **Consolidação**: O JSON deve conter OBRIGATORIAMENTE uma chave "resumo_executivo" com os totais finais.
            4. **Sintese**: Adicione uma chave "sintese" com uma descrição curta (1 parágrafo) do que foi encontrado.

            REQUISITO DE SAÍDA:
            Retorne APENAS o objeto JSON puro contendo "resumo_executivo" e "sintese". Não use markdown, não adicione explicações fora do JSON.
            """
        ],
        tools=tools,
        debug_mode=True,
    )
