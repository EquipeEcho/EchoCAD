from agno.agent import Agent
from agno.team import Team
from agno.models.ollama import Ollama

from .entity_dxf import EntityDxf


def create_team(entity: EntityDxf, model_id: str, members: list[Agent | Team], options: dict[str, int | float] = {}):
    """
    Factory function to create the Echo Team with its agents.
    This facilitates memory discharge as agents are created per session/request.
    """

    team = Team(
        name="Echo Team",
        model=Ollama(
            id=model_id,
            options=options
        ),
        members=members,
        instructions=[
            'formato esperado pelo classificator_agent = {disciplina:str, layers:[str]}'
        ],
        markdown=True,
        use_json_mode=True,
        tools=[entity.get_layers, entity.check_exists,
               entity.get_types_in_layers, entity.get_entities_by_layer],
        debug_mode=True,
    )

    return team
