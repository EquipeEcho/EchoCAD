from agno.agent import Agent
from agno.models.ollama import Ollama
from pydantic import BaseModel, Field


class LayerSelectionOutput(BaseModel):
    layers: list[str] = Field(...,
                              description="Layers selecionados da lista original.")


def create_classificator_agent(tools):
    return Agent(
        id='agent-leyer-select',
        name='Agent Layer Select',
        role='Seleciona os layers relevantes dentre uma lista de layers existentes em um projeto baseado na disciplina de engenharia fornecida',
        description='Selecione os layers baseado em disciplina de engenharia.',
        model=Ollama(
            id='qwen2.5:7b',
            options={
                "temperature": 0,
                "num_ctx": 1024,
            }
        ),
        instructions=[
            '''
            Você é um especialista em automação de projetos CAD/DXF. Sua tarefa é filtrar uma lista de layers baseando-se em uma disciplina de engenharia específica.

            ### REGRAS DE CLASSIFICAÇÃO (Dicionário de Disciplinas):
            1. ALVENARIA/ARQUITETURA: 'arq-', 'alv-', 'parede', 'muro', 'divisoria', 'revestimento', 'porta', 'janela'.
            2. ELÉTRICA: 'ele-', 'eletrica', 'luz', 'tomada', 'iluminacao', 'quadro', 'duto', 'conduite', 'fio', 'cabo'.
            3. HIDRÁULICA (ÁGUA FRIA/QUENTE): 'hid-', 'af-', 'aq-', 'agua', 'prumada', 'coluna', 'registro', 'misturador'.
            4. ESGOTO/PLUVIAL: 'esg-', 'pluv-', 'esgoto', 'tubulacao', 'caixa-gordura', 'ralo', 'ventilacao', 'calha'.
            5. INCÊNDIO: 'inc-', 'fire-', 'hidrante', 'sprinkler', 'extintor', 'sinalizacao', 'alarme'.
            6. PAISAGISMO: 'pai-', 'paisag-', 'grama', 'arvore', 'vegetacao', 'canteiro', 'jardim'.
            7. LÓGICA/TI: 'log-', 'dados', 'rack', 'wifi', 'fibra', 'cat6', 'telefonia'.
            8. INFRAESTRUTURA (TERRAPLANAGEM/DEMOLIÇÃO): 'ter-', 'terra-', 'corte', 'aterro', 'nivel', 'demol-'.

            ### RESTRIÇÕES CRÍTICAS:
            - Utilize a tool correta para obter a lista bruta de layers válidos.
            - Proibido inventar ou corrigir nomes.
            - Se nenhum layer corresponder à disciplina, retorne uma lista vazia: [].
            - A saída deve ser estritamente uma list(str) de Python.
            - PROIBIDO incluir explicações, saudações, introduções ou qualquer texto adicional.
            '''
        ],
        tools=tools,
        debug_mode=True,
        # input_schema=LayerSelectionInput,
        output_schema=LayerSelectionOutput,
    )
