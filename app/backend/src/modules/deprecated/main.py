import os
import json
from pathlib import Path
from datetime import datetime
from app.backend.src.modules.deprecated.entity_dxf import EntityDxf
from app.backend.src.modules.deprecated.team_ai import create_team
from app.backend.src.modules.deprecated.agents.agent_context import create_context_agent
from app.backend.src.modules.deprecated.agents.agent_layer_select import create_classificator_agent
from app.backend.src.modules.deprecated.agents.agent_spatial_analyst import create_spatial_analyst_agent
from app.backend.src.modules.deprecated.agents.agent_surveyor import create_surveyor_agent
from app.backend.src.modules.deprecated.tools.memorial_populator import MemorialPopulator


def run_extraction(prompt_usuario: str, dxf_path: str, project_id: int, gerar_excel: bool = True):
    print(f"\n=== INICIANDO EXTRAÇÃO ECHO TEAM ===\n")
    print(f"Prompt do Usuário: {prompt_usuario}")
    print(f"Projeto ID: {project_id}")
    
    # 0. Inicialização do DXF
    if not os.path.exists(dxf_path):
        print(f"Erro: Arquivo {dxf_path} não encontrado.")
        return {"erro": f"Arquivo {dxf_path} não encontrado."}
    
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
    
    resultado = {
        "json": response.content,
        "arquivo_excel": None
    }
    
    # 4. Geração do Excel (opcional)
    if gerar_excel:
        try:
            resultado_excel = _gerar_excel_a_partir_json(response.content, prompt_usuario, project_id)
            resultado["arquivo_excel"] = resultado_excel
            print(f"\n✓ Excel gerado com sucesso: {resultado_excel}")
        except Exception as e:
            print(f"\n✗ Erro ao gerar Excel: {str(e)}")
            resultado["erro_excel"] = str(e)
    
    print("\n=== PROCESSO FINALIZADO ===")
    return resultado


def _gerar_excel_a_partir_json(json_resultado: str, prompt_usuario: str, project_id: int) -> str:
    """
    Extrai os dados do JSON e popula um template Excel.
    
    Args:
        json_resultado: String JSON com os resultados
        prompt_usuario: Prompt original para determinar a disciplina
        project_id: ID do projeto para salvar em pasta correta
        
    Returns:
        Caminho relativo do arquivo Excel gerado (para salvar no BD)
    """
    try:
        # Parse do JSON
        dados = json.loads(json_resultado)
    except json.JSONDecodeError:
        # Se não for JSON puro, tenta extrair
        print("Aviso: Resultado não é JSON válido, tentando extrair estrutura...")
        dados = {"dados_brutos": json_resultado}
    
    # Determina a disciplina a partir do prompt
    prompt_lower = prompt_usuario.lower()
    disciplina = "indefinido"
    
    if any(word in prompt_lower for word in ["parede", "alvenaria", "alv", "arq"]):
        disciplina = "alvenaria"
    elif any(word in prompt_lower for word in ["elétric", "elet", "fio", "circuito", "luz"]):
        disciplina = "eletrica"
    elif any(word in prompt_lower for word in ["hidráulic", "hid", "água", "cano", "esgoto"]):
        disciplina = "hidraulica"
    elif any(word in prompt_lower for word in ["rede", "dados", "telefone", "net"]):
        disciplina = "rede"
    
    # Paths dos templates e saída
    template_path = Path(__file__).parent.parent.parent / "templates" / "memorial_model.xlsx"
    
    # Salvar em pasta do projeto (como fazem com uploads de DXF)
    backend_root = Path(__file__).parent.parent.parent.parent
    uploads_dir = backend_root / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    project_dir = uploads_dir / str(project_id)
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Nome do arquivo de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memorial_{disciplina}_{timestamp}.xlsx"
    output_path = project_dir / filename
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_path}")
    
    # Popula o Excel
    populator = MemorialPopulator(str(template_path), str(output_path))
    
    if disciplina == "alvenaria":
        # Para alvenaria, extrai summary_data se disponível
        summary_data = dados.get("resumo_executivo", {})
        if summary_data:
            populator.populate_alvenaria(summary_data)
    elif disciplina == "eletrica":
        # Para elétrica, extrai síntese ou clusters
        synthesis_data = dados.get("sintese", dados)
        populator.populate_eletrica(synthesis_data)
    
    # Adiciona informações gerais na planilha
    if hasattr(populator.wb, 'active'):
        ws_info = populator.wb.active
        ws_info.cell(row=1, column=1).value = f"Disciplina: {disciplina.upper()}"
        ws_info.cell(row=2, column=1).value = f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    
    populator.save()
    
    # Retornar caminho relativo para salvar no banco de dados
    relative_path = f"{project_id}/{filename}"
    return relative_path