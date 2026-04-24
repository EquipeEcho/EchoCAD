import asyncio
import logging
# from pydantic import BaseModel
from pathlib import Path
from agno.agent import Agent
# from agno.models.ollama import Ollama
from agno.models.groq import Groq

from tools.layer_tools import LayerTools

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

layer = LayerTools(Path(__file__).parent/'teste_ofc.dxf')

logger.debug(f"Layer names: {layer.get_layers()}")

agent = Agent(
    name='Engineer_1',
    # model=Ollama(id="qwen2.5"),
    model=Groq(id="llama-3.1-8b-instant"),
    description="You help people with your tools, use only tool you can",
    instructions="Layer names are unique identifiers; do not rename them.",
    tools=[layer.get_layers],
)

response = asyncio.run(agent.arun(input()))
print(response.content)
