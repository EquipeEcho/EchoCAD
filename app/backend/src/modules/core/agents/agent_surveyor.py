from agno.agent import Agent
from agno.models.ollama import Ollama


def create_surveyor_agent(tools: list):
    return Agent(
        id='quantity-surveyor',
        name='Quantity Surveyor',
        role='Realiza a contagem de quantitativos e síntese final do projeto de engenharia',
        description='Consolida dados de contagem e gera um JSON estruturado final.',
        model=Ollama(
            id='qwen2.5:3b',
            options={
                "temperature": 0.0,
                "num_ctx": 2048,
            }
        ),
        instructions=[
            '''
            Você é um Engenheiro Orçamentista sênior especialista em extração de dados CAD.
            Sua tarefa é consolidar todas as informações coletadas pelos outros agentes em um JSON final de alta precisão.

            REGRAS DE CÁLCULO OBRIGATÓRIAS:
            1. **Alvenaria**: Calcule a Área Total (m2) = (Soma de todos os total_length) * 3.0. Retorne tanto o comprimento quanto a área.
            2. **Elétrica**: Some os comprimentos de todos os clusters para obter a metragem total de fios/cabos.
            3. **Consolidação**: O JSON deve ter uma chave "resumo_executivo" com os totais finais por disciplina.
            4. **Unidades**: Use 'm' para comprimentos, 'm2' para áreas e 'un' para contagem de blocos/textos.

            REQUISITO DE SAÍDA:
            Retorne APENAS o objeto JSON puro. Não use markdown, não adicione explicações.

            '''
        ],
        tools=tools,
        debug_mode=True,
    )
