from agno.team import Team
from pathlib import Path

from .entity_dxf import EntityDxf
from .tools.layer_tools import LayerTools 
from .agents import layer_select_agent, context_agent, model_provider

def create_echo_team(dxf_path: str, model_type="strong"):
    """
    Factory function to create the Echo Team with its agents.
    This facilitates memory discharge as agents are created per session/request.
    """
    
    # 1. Load the DXF and tools
    layer_manager = EntityDxf(Path(dxf_path))
    tools = LayerTools(layer_manager)
    
    # 2. Select Models
    # You can easily toggle between Groq and Ollama here
    if model_type == "privacy":
        main_model = model_provider.privacity_model
    else:
        main_model = model_provider.strong_model
        
    # 3. Instantiate Agents using their factory functions
    # Context Agent uses a faster model usually, or the same as the team
    ctx_agent = context_agent.get_context_agent(model=model_provider.fast_model)
    
    # Selector Agent MUST use the tools to avoid hallucination
    selector = layer_select_agent.get_selector_agent(
        model=model_provider.text_comprehension, 
        tools=[tools.get_layers, tools.check_exists]
    )

    # 4. Create the Team
    echoteam = Team(
        name="Echo Team",
        model=model_provider.privacity_model,
        members=[ctx_agent, selector],
        instructions=[
            "1. Primeiro, chame o ContextAgent para analisar o prompt do usuário e entender a disciplina da obra.",
            "2. Em seguida, o Layer Selector Agent DEVE usar a ferramenta 'get_layers' para ver quais layers REALMENTE existem no DXF.",
            "3. O Layer Selector Agent filtrará os layers baseando-se no contexto gerado pelo ContextAgent.",
            "4. A resposta final deve conter a lista exata de nomes de layers encontrados.",
        ],
        markdown=True,
    )
    
    return echoteam

# Example of how to use it (can be moved to a main.py or route)
if __name__ == "__main__":
    dxf_file = Path(__file__).parent / 'teste.dxf'
    team = create_echo_team(str(dxf_file))
    team.print_response("Este projeto é sobre uma instalação elétrica industrial. Selecione os layers relevantes.", stream=True)
