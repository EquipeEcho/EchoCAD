import sys
from pathlib import Path

# Adiciona o diretório backend ao sys.path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from src.modules.core.entity_dxf import EntityDxf
from src.modules.core.team_ai import create_team
from src.modules.core.agents.agent_context import create_context_agent
from src.modules.core.agents.agent_layer_select import create_classificator_agent
from src.modules.core.agents.agent_spatial_analyst import create_spatial_analyst_agent
from src.modules.core.agents.agent_surveyor import create_surveyor_agent

def test_backend_analysis():
    file_path = backend_path / "uploads" / "teste.dxf"
    if not file_path.exists():
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    print(f"Iniciando teste de análise para: {file_path}")
    
    entity = EntityDxf(file_path)
    
    # Criar agentes
    context_agent = create_context_agent()
    layer_agent = create_classificator_agent(tools=[]) 
    spatial_agent = create_spatial_analyst_agent(tools=[])
    surveyor_agent = create_surveyor_agent(tools=[])

    # Criar time
    team = create_team(entity, [context_agent, layer_agent, spatial_agent, surveyor_agent])

    print("Executando análise (Maestro coordenando)...")
    
    # Executar análise
    response = team.run("Analise a planta do tipo 'elétrica' no arquivo 'teste.dxf'.")
    
    print("\n--- RESULTADO FINAL ---")
    print(response.content)
    print("------------------------")

if __name__ == "__main__":
    test_backend_analysis()
