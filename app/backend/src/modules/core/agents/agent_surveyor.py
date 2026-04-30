from agno.agent import Agent
from agno.models.groq import Groq

def create_surveyor_agent(tools):
    return Agent(
        id='quantity-surveyor',
        name='Quantity Surveyor',
        role='Realiza a contagem de quantitativos e síntese final do projeto de engenharia',
        description='Consolida dados de contagem e gera o arquivo Excel final.',
        model=Groq(
            id='llama-3.3-70b-versatile',
            temperature=0,
        ),
        instructions=[
            '''
            Você é um Engenheiro Orçamentista sênior.
            Sua tarefa é gerar o relatório quantitativo e POPULAR o arquivo Excel de memorial.

            FLUXO DE TRABALHO:
            1. Use `get_grouped_entities_summary` para visão geral.
            2. Consolide as informações do `Spatial Analyst`.
            3. Após gerar a síntese, use a tool `run_population` para gravar os dados no Excel.

            CONFIGURAÇÕES PARA run_population:
            - template: "C:/Users/ADS_DSM/.projects/EchoCAD/app/backend/src/modules/Memorial/model_memorial.xlsx"
            - output: "C:/Users/ADS_DSM/.projects/EchoCAD/app/backend/src/modules/Memorial/memorial_preenchido.xlsx"
            - data_json: O JSON com os quantitativos extraídos.
            - discipline: A disciplina identificada.

            SAÍDA FINAL:
            Um JSON completo com a síntese E a confirmação de que o Excel foi gerado.
            '''
        ],
        tools=tools,
        debug_mode=True,
    )

