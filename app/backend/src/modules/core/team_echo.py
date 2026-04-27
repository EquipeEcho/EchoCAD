from agno.team import Team
from pathlib import Path

from .entity_dxf import EntityDxf
from .tools.layer_tools import LayerTools 
from .agents import layer_select_agent, context_agent, model_provider

# Load the DXF file
dxf_file_path = Path(__file__).parent / 'teste.dxf'
layer = EntityDxf(dxf_file_path)
tools = LayerTools(layer)

# Get specialized agents
# Use strong_model for selector because it uses tools
selector = layer_select_agent.get_selector_agent([tools.get_layers, tools.check_exists])
selector.model = model_provider.strong_model

echoteam = Team(
    name="Echo Team",
    model=model_provider.strong_model,
    members=[
        context_agent.context_agent,
        selector,
    ],
    instructions=[
        "1. Chame o ContextAgent para resumir o projeto.",
        "2. Com o resumo, chame o Layer Selector Agent para identificar os layers REAIS no DXF.",
        "3. O Layer Selector Agent DEVE usar a ferramenta 'get_layers' para ver os layers reais.",
        "4. Retorne a resposta final com os nomes exatos dos layers.",
    ],
    markdown=True,
)
