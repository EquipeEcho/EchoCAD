from agno.agent import Agent
from agno.team import Team
from agno.models.groq import Groq

from .entity_dxf import EntityDxf
from .tools.memorial_populator import run_population

def create_team(entity: EntityDxf, members: list[Agent | Team]):
    """
    Factory function to create the Echo Team with its agents.
    Exposes full DXF analysis and Excel population tools.
    """

    team = Team(
        name="Echo Team",
        model=Groq(
            id='llama-3.3-70b-versatile',
            temperature=0.2
        ),
        members=members,
        instructions=[
            "Você é o coordenador do EchoCAD AI Team.",
            "O fluxo de trabalho deve ser:",
            "1. Identificar as disciplinas com o ContextAgent.",
            "2. Selecionar os layers REAIS com o Agent Layer Select.",
            "3. Se houver necessidade de análise de conectividade (fios, tubos, paredes), use o Spatial Analyst.",
            "4. Finalize com o Quantity Surveyor para gerar o JSON quantitativo e popular o Excel com run_population.",
            "Garanta que o Quantity Surveyor tenha acesso a todos os dados antes de chamar a população."
        ],
        markdown=True,
        # use_json_mode=True, 
        tools=[
            entity.get_layers, 
            entity.get_grouped_entities_summary,
            entity.get_detailed_entities,
            entity.get_connectivity_graph,
            entity.find_text_near_entities,
            run_population
        ],
        debug_mode=True,
    )

    return team

