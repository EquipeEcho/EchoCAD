from agno.agent import Agent
from agno.team import Team
from agno.models.ollama import Ollama

from .entity_dxf import EntityDxf

# def set_project_context(run_context: RunContext, discipline: str = None, layers: list = None) -> str:
#     """Armazena a disciplina e os layers selecionados no estado global da sessão."""
#     if discipline:
#         run_context.session_state["discipline"] = discipline
#     if layers:
#         run_context.session_state["selected_layers"] = layers
#     return f"Contexto atualizado: Disciplina={run_context.session_state.get('discipline')}, Layers={run_context.session_state.get('selected_layers')}"

def create_team(entity: EntityDxf, members: list[Agent | Team]):
    # Define as ferramentas disponíveis para os agentes a partir do EntityDxf
    dxf_tools = [
        entity.get_layers,
        entity.check_exists,
        entity.get_grouped_entities_summary,
        entity.get_detailed_entities,
        entity.get_connectivity_graph,
        entity.find_text_near_entities
    ]

    # Atualiza as ferramentas de cada agente se elas não foram injetadas
    for member in members:
        if isinstance(member, Agent):
            member.tools = dxf_tools

    team = Team(
        name="Echo Team",
        model=Ollama(
            id='qwen2.5:7b',
            options={
                "temperature": 0,
                "num_ctx": 8192,
            }
        ),
        members=members,
        instructions=[
            "VOCÊ É O MAESTRO TÉCNICO. SEU TRABALHO É EXECUTAR UM PIPELINE RÍGIDO DE 4 ETAPAS SEM REPETIÇÕES.",
            "PROIBIDO CONVERSAR COM O USUÁRIO OU EXPLICAR PASSOS.",
            
            "ORDEM OBRIGATÓRIA E ÚNICA DE EXECUÇÃO:",
            "1. CONTEXTO: Peça ao ContextAgent para definir a disciplina exata.",
            "2. FILTRAGEM: Com a disciplina, peça ao Agent Layer Select a lista de layers reais (JSON).",
            "3. ANÁLISE: Com os layers, peça ao Spatial Analyst o resumo técnico da conectividade.",
            "4. SÍNTESE: Com o resumo da análise, peça ao Quantity Surveyor o JSON final consolidado.",
            
            "REGRA CRÍTICA: Cada agente deve ser chamado exatamente uma vez na ordem acima.",
            "RESPOSTA FINAL: Entregue EXCLUSIVAMENTE o JSON puro gerado pelo Quantity Surveyor. Nada mais."
        ],
        markdown=False,
        debug_mode=True,
    )
    return team

# "Você é o Maestro do EchoCAD. Use o TeamMode.tasks para processar o pedido.",
# "FLUXO OBRIGATÓRIO:",
# "1. Crie tarefas com `create_task`. Use títulos curtos: 'contexto', 'layers', 'analise', 'quantitativo'.",
# "2. IMPORTANTE: Ao usar `execute_task`, use o ID retornado (ex: 'e7bbb6d3'), NÃO use o título.",
# "3. Salve a disciplina e os layers no session_state usando `set_project_context` após as respectivas tarefas.",
# "4. A tarefa final do Quantity Surveyor deve gerar APENAS o JSON.",
# "A resposta final do time deve ser exclusivamente o JSON puro do Quantity Surveyor."