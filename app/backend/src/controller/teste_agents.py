from pathlib import Path

from ..modules.core.entity_dxf import EntityDxf

# seus agentes
from ..modules.core.agents.agent_context import create_context_agent
from ..modules.core.agents.agent_layer_select import create_classificator_agent
from ..modules.core.agents.agent_spatial_analyst import create_spatial_analyst_agent
from ..modules.core.agents.agent_surveyor import create_surveyor_agent


def run_agents_test(dxf_path: str):
    """
    Executa todos os agentes disponíveis em um fluxo simples de teste.
    """

    if not Path(dxf_path).exists():
        return {"error": "Arquivo DXF não encontrado"}

    # 1. Instanciar entidade DXF
    entity = EntityDxf(dxf_path)

    # 2. Obter layers reais
    layers = entity.get_layers()

    # 3. CONTEXT AGENT
    context_agent = create_context_agent()
    disciplina = context_agent.run(f"Classifique as disciplinas com base nesses layers: {layers}").content

    # 4. LAYER AGENT
    layer_agent = create_classificator_agent()
    layer_agent.set_tools([
        entity.get_layers,
    ])
    

    # erro de validação de input
    selected_layers = layer_agent.run({
        "disciplina": disciplina,
        "layers": layers
    })

    # 5. SPATIAL AGENT
    spatial_agent = create_spatial_analyst_agent(
        tools=[
            entity.get_connectivity_graph # ver se essa tool existe
        ]
    )

    spatial_analysis = spatial_agent.run({
        "layers": selected_layers
    })

    # 6. SURVEYOR AGENT
    surveyor_agent = create_surveyor_agent(
        tools=[]
    )

    final_result = surveyor_agent.run({
        "disciplina": disciplina,
        "analysis": spatial_analysis
    })

    return {
        "disciplina": disciplina,
        "selected_layers": selected_layers,
        "spatial_analysis": spatial_analysis,
        "final_result": final_result
    }