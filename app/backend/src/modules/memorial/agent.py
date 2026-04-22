import asyncio
from pydantic import BaseModel
from pathlib import Path
from agno.agent import Agent
from agno.models.ollama import Ollama

from tools.layer_tools import LayerTools


layer = LayerTools(Path(__file__).parent/'teste.dxf')

print(layer.get_layers())


agent = Agent(
    name='Engineer_1',
    model=Ollama(id="qwen2.5"),
    description="You help people with your tools",
    instructions="Layer names are unique identifiers; do not rename them.",
    tools=[layer.get_layers],
)

response = asyncio.run(agent.arun(
    "Quais os layes estão disponíveis no arquivo?"))
print(response.content)
