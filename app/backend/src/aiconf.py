import os
from agno.models.groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


quick_model = Groq(
    id="openai/gpt-oss-20b",
    name="quick_model",
    api_key=""
)

medium_model = Groq(
    id="openai/gpt-oss-20b",
    name="medium_model",
    api_key=""
)

high_model = Groq(
    id="openai/gpt-oss-20b",
    name="high_model",
    api_key=""
)