import logging
from pathlib import Path
from sqlalchemy.orm import Session
from src.models.projeto_db import Projeto, Planta
from src.modules.core.team_ai import create_team
from src.modules.core.entity_dxf import EntityDxf
from src.modules.core.agents.agent_context import create_context_agent
from src.modules.core.agents.agent_layer_select import create_classificator_agent
from src.modules.core.agents.agent_spatial_analyst import create_spatial_analyst_agent
from src.modules.core.agents.agent_surveyor import create_surveyor_agent

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self, db: Session):
        self.db = db

    def run_analysis_for_project(self, project_id: int):
        """
        Orquestra a análise para todas as plantas de um projeto.
        """
        project = self.db.query(Projeto).filter(Projeto.id == project_id).first()
        if not project:
            raise ValueError(f"Projeto {project_id} não encontrado")

        results = []
        for planta in project.plantas_cad:
            try:
                result = self.analyze_planta(planta)
                results.append({
                    "planta_id": planta.id,
                    "arquivo": planta.arquivo,
                    "resultado": result
                })
            except Exception as e:
                logger.error(f"Erro ao analisar planta {planta.id}: {e}")
                results.append({
                    "planta_id": planta.id,
                    "error": str(e)
                })
        
        return results

    def analyze_planta(self, planta: Planta):
        """
        Executa o TeamAI para uma única planta.
        """
        # 1. Localizar o arquivo
        file_path = Path("uploads") / (planta.arquivo or "")
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo DXF não encontrado em {file_path}")

        # 2. Instanciar EntityDxf
        entity = EntityDxf(file_path)

        # 3. Preparar Agentes (As ferramentas serão injetadas pelo create_team)
        context_agent = create_context_agent()
        # O agent_layer_select define create_classificator_agent
        layer_agent = create_classificator_agent(tools=[]) 
        spatial_agent = create_spatial_analyst_agent(tools=[])
        surveyor_agent = create_surveyor_agent(tools=[])

        # 4. Criar o Time (Maestro)
        team = create_team(entity, [context_agent, layer_agent, spatial_agent, surveyor_agent])

        # 5. Executar o Pipeline
        response = team.run(f"Analise a planta do tipo '{planta.tipo}' no arquivo '{planta.arquivo}'.")

        return response.content
