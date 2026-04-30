from agno.agent import Agent
from agno.models.groq import Groq
from pydantic import BaseModel, Field

class LayerSelectionOutput(BaseModel):
    layers: list[str] = Field(...,
                              description="Layers selecionados da lista original.")

def create_classificator_agent(tools):
    # Garantir que tools seja uma lista para o Agent
    if not isinstance(tools, list):
        tools = [tools]

    return Agent(
        id='agent-layer-select',
        name='Agent Layer Select',
        role='Seleciona os layers relevantes de um projeto CAD baseado na disciplina de engenharia',
        description='Filtra a lista real de layers de um arquivo DXF usando regras de palavras-chave por disciplina.',
        model=Groq(
            id='llama-3.3-70b-versatile',
            temperature=0,
        ),
        instructions=[
            '''
            Você é um especialista em automação de projetos CAD/DXF.
            Sua única tarefa é filtrar a lista REAL de layers de um arquivo.

            FLUXO DE TRABALHO OBRIGATÓRIO:
            1. Você DEVE SEMPRE chamar a tool `get_layers` primeiro para obter os nomes dos layers existentes no projeto.
            2. Compare cada layer retornado pela tool com as REGRAS DE CLASSIFICAÇÃO abaixo.
            3. Selecione apenas os layers da lista real que contenham os termos ou prefixos indicados.
            4. Se nenhum layer da lista real corresponder, retorne uma lista vazia [].

            ### REGRAS DE CLASSIFICAÇÃO (Termos de busca):
            1. ALVENARIA/ARQUITETURA: 'arq-', 'alv-', 'parede', 'muro', 'divisoria', 'revestimento', 'porta', 'janela'.
            2. ELÉTRICA: 'ele-', 'eletrica', 'luz', 'tomada', 'iluminacao', 'quadro', 'duto', 'conduite', 'fio', 'cabo'.
            3. HIDRÁULICA (ÁGUA FRIA/QUENTE): 'hid-', 'af-', 'aq-', 'agua', 'prumada', 'coluna', 'registro', 'misturador'.
            4. ESGOTO/PLUVIAL: 'esg-', 'pluv-', 'esgoto', 'tubulacao', 'caixa-gordura', 'ralo', 'ventilacao', 'calha'.
            5. INCÊNDIO: 'inc-', 'fire-', 'hidrante', 'sprinkler', 'extintor', 'sinalizacao', 'alarme'.
            6. PAISAGISMO: 'pai-', 'paisag-', 'grama', 'arvore', 'vegetacao', 'canteiro', 'jardim'.
            7. LÓGICA/TI: 'log-', 'dados', 'rack', 'wifi', 'fibra', 'cat6', 'telefonia'.
            8. INFRAESTRUTURA (TERRAPLANAGEM/DEMOLIÇÃO): 'ter-', 'terra-', 'corte', 'aterro', 'nivel', 'demol-'.

            ### RESTRIÇÕES CRÍTICAS:
            - NÃO invente nomes de layers. Use APENAS os nomes retornados pela tool `get_layers`.
            - Os termos acima são apenas para IDENTIFICAÇÃO. O resultado final deve ser uma lista dos layers REAIS.
            - Responda APENAS com um objeto JSON no formato: {"layers": ["layer1", "layer2"]}
            - PROIBIDO incluir explicações, saudações ou qualquer texto fora do JSON.
            '''
        ],
        tools=tools,
        debug_mode=True,
    )
