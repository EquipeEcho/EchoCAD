from agno.agent import Agent
from agno.team import Team
from agno.models.ollama import Ollama

from .entity_dxf import EntityDxf


def create_echo_team(entity: EntityDxf, model_id: str, members: list[Agent | Team], options: dict[str, int | float] = {}):
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
        instructions=[],
        markdown=True,
        tools=[entity.get_layers]
    )

    return team
