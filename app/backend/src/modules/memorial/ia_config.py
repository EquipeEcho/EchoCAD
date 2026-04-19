import json
import re
import json

from agno.agent import Agent
from agno.models.ollama import Ollama

classifier = Agent(
    model=Ollama(id="qwen2.5:8b"),
    instructions=[
        '''
        Você é um classificador de elementos de projetos CAD.
        Classifique em UMA das categorias:
        - parede
        - cotas
        - cobertura
        - vão
        - ambiente_nome
        - elétrica
        - hidro
        - estrutural
        - desconhecido

        Responda em JSON:
        {{"tipo": "...", "confianca": 0.0}}'''],
    markdown=False
)


def classificar(nome: str, layer: str, texto: str, tipo_entidade: str):
    """Executa o LLM com os parâmetros fornecidos."""
    response = classifier.run(
        f"Elemento: nome: {nome} layer: {layer} texto: {texto} tipo: {tipo_entidade}", stream=True)
    return extrair_json(response)

def extrair_json(resposta):
    try:
        # pega o primeiro bloco JSON da string
        match = re.search(r'\{.*\}', resposta, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except:
        pass

    return None


def heuristica(elemento):
    nome = elemento["nome"].upper()

    if "TOM" in nome:
        return "tomada", 0.95
    if "LUM" in nome:
        return "luminaria", 0.95

    return None
