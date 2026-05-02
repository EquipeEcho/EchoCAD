import os
from dotenv import load_dotenv
from entity_dxf import EntityDxf
from team_ai import create_team
from agents.agent_context import create_context_agent
from agents.agent_layer_select import create_classificator_agent
from agents.agent_spatial_analyst import create_spatial_analyst_agent
from agents.agent_surveyor import create_surveyor_agent

# Configuração de ambiente
load_dotenv('.env')
if os.getenv('API_KEY') and not os.getenv('GROQ_API_KEY'):
    os.environ['GROQ_API_KEY'] = os.getenv('API_KEY')

def run_extraction(prompt_usuario: str):
    print(f"\n=== INICIANDO EXTRAÇÃO ECHO TEAM ===\n")
    print(f"Prompt do Usuário: {prompt_usuario}")
    
    # 0. Inicialização do DXF
    dxf_path = 'projeto_completo_treino.dxf'
    if not os.path.exists(dxf_path):
        print(f"Erro: Arquivo {dxf_path} não encontrado.")
        return
    
    dxf = EntityDxf(dxf_path)
    
    # 1. Criação dos Agentes
    agente_contexto = create_context_agent()
    agente_layer_select = create_classificator_agent([dxf.get_layers, dxf.check_exists])
    agente_espacial = create_spatial_analyst_agent([dxf.get_connectivity_graph])
    agente_surveyor = create_surveyor_agent([
        dxf.get_grouped_entities_summary,
        dxf.get_detailed_entities
    ])

    # 2. Criação do Team
    team = create_team(dxf, [
        agente_contexto, 
        agente_layer_select, 
        agente_espacial, 
        agente_surveyor
    ])

    # 3. Execução
    response = team.run(prompt_usuario)
    
    print("\n--- RESULTADO FINAL (JSON) ---")
    print(response.content)
    print("\n=== PROCESSO FINALIZADO ===")

if __name__ == "__main__":
    # Teste para Alvenaria
    run_extraction("preciso do levantamento quantitativo de todas as paredes (alvenaria) do projeto")
