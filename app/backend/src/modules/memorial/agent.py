import asyncio
import random
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.ollama import Ollama

from app.backend.src.modules.memorial.tools.layer_tools import get_layers


def get_weather(city: str) -> str:
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    return f"The weather in {city} is {random.choice(weather_conditions)}."

class WeatherResponse(BaseModel):
    # output_schema=WeatherResponse # use this on agent.arun
    city: str
    weather: str

agent = Agent(
    name='Engineer_1',
    model=Ollama(id="qwen2.5"),
    description="You help people with your tools",
    instructions="Layer names are unique identifiers; do not rename them.",
    tools=[get_layers],
)

response = asyncio.run(agent.arun("Quais os layes estão disponíveis no arquivo? Path = '/data/highbackup/@projetos/echocad/app/backend/src/modules/memorial/teste.dxf'"))
# print(response)
print(response.content)