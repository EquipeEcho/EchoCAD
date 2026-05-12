import json
import logging
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session
from src.models.projeto_db import Project, Planta
from app.backend.src.modules.deprecated.team_ai import create_team
from app.backend.src.modules.deprecated.entity_dxf import EntityDxf
from app.backend.src.modules.deprecated.agents.agent_context import create_context_agent
from app.backend.src.modules.deprecated.agents.agent_layer_select import create_classificator_agent
from app.backend.src.modules.deprecated.agents.agent_spatial_analyst import create_spatial_analyst_agent
from app.backend.src.modules.deprecated.agents.agent_surveyor import create_surveyor_agent

logger = logging.getLogger(__name__)

# Base path do backend (onde fica a pasta uploads e results)
BACKEND_ROOT = Path(__file__).parent.parent.parent
RESULTS_PATH = BACKEND_ROOT / "results"
UPLOADS_PATH = BACKEND_ROOT / "uploads"

RESULTS_PATH.mkdir(parents=True, exist_ok=True)
UPLOADS_PATH.mkdir(parents=True, exist_ok=True)

class AIOrchestrator:
    # Lock global para evitar processamentos simultâneos
    _lock = asyncio.Lock()

    def __init__(self, db: Session):
        self.db = db

    async def run_analysis_for_project(self, project_id: int, stream: bool = False):
        """
        Orquestra a análise para todas as plantas de um projeto.
        """
        # A checagem de lock já é feita na rota, mas reforçamos aqui
        if self._lock.locked():
            raise RuntimeError("Já existe um processamento de IA em andamento. Por favor, aguarde.")

        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Projeto {project_id} não encontrado")

        if stream:
            return self._stream_project_analysis(project)

        # Para modo não-stream, usamos o lock via context manager
        async with self._lock:
            return await asyncio.to_thread(self._run_sync_analysis, project)

    def _run_sync_analysis(self, project: Project):
        results = []
        for planta in project.blueprint:
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
        
        # Salvar resultado final em JSON
        self.save_results(project.id, results)
        return results

    async def _stream_project_analysis(self, project: Project):
        """
        Gera um stream de eventos do processamento.
        """
        async with self._lock:
            project_results = []
            for planta in project.blueprint:
                yield f"data: Iniciando análise da planta {planta.arquivo} ({planta.tipo})\n\n"
                
                try:
                    # 1. Localizar o arquivo usando o caminho salvo no banco (projeto_id/arquivo.dxf)
                    relative_path = (planta.arquivo or "").strip()
                    file_path = UPLOADS_PATH / relative_path

                    yield f"data: Buscando em: {file_path.absolute()}\n\n"

                    if not file_path.exists():
                        # Tentativa 2: Tentar caminho relativo ao CWD caso o BACKEND_ROOT tenha falhado
                        alt_path = Path("uploads") / relative_path
                        yield f"data: Não encontrado. Tentando alternativa: {alt_path.absolute()}\n\n"
                        if alt_path.exists():
                            file_path = alt_path
                        else:
                            # Tentativa 3: Se não tiver a barra (legado), tenta na raiz de uploads
                            if "/" not in relative_path:
                                legacy_path = UPLOADS_PATH / relative_path
                                if legacy_path.exists():
                                    file_path = legacy_path
                                else:
                                    yield f"data: ERRO: Arquivo {relative_path} não encontrado em nenhuma das localizações.\n\n"
                                    continue
                            else:
                                yield f"data: ERRO: Arquivo {relative_path} não encontrado em nenhuma das localizações.\n\n"
                                continue
                    # 2. Instanciar EntityDxf
                    entity = EntityDxf(file_path)

                    # 3. Preparar Agentes
                    context_agent = create_context_agent()
                    layer_agent = create_classificator_agent(tools=[]) 
                    spatial_agent = create_spatial_analyst_agent(tools=[])
                    surveyor_agent = create_surveyor_agent(tools=[])

                    # 4. Criar o Time
                    team = create_team(entity, [context_agent, layer_agent, spatial_agent, surveyor_agent])

                    # 5. Executar com stream
                    yield f"data: EXECUTANDO: Maestro coordenando agentes...\n\n"
                    full_response = ""
                    # Agno Team.run with stream=True returns an iterator of RunResponse
                    # Agno Team.run is sync, so we wrap it or use it carefully in async
                    loop = asyncio.get_event_loop()
                    
                    # Para simplificar o stream que já é um gerador, vamos rodar o team.run normalmente
                    # mas o processamento interno pode demorar.
                    for response_chunk in team.run(f"Analise a planta do tipo '{planta.tipo}' no arquivo '{planta.arquivo}'.", stream=True):
                        if hasattr(response_chunk, 'content') and response_chunk.content:
                            content = response_chunk.content
                        elif isinstance(response_chunk, str):
                            content = response_chunk
                        else:
                            continue
                        
                        full_response += content
                        # Escapar quebras de linha para não quebrar o protocolo SSE
                        safe_content = content.replace("\n", "\\n")
                        yield f"data: {safe_content}\n\n"

                    project_results.append({
                        "planta_id": planta.id,
                        "arquivo": planta.arquivo,
                        "resultado": full_response
                    })
                    yield f"data: Planta {planta.arquivo} concluída.\n\n"

                except Exception as e:
                    logger.error(f"Erro no stream: {e}")
                    yield f"data: ERRO CRÍTICO: {str(e)}\n\n"

            # Salvar ao final do stream
            self.save_results(project.id, project_results)
            yield f"data: [DONE] Processamento concluído para o projeto {project.id}\n\n"

    def analyze_planta(self, planta: Planta):
        """
        Executa o TeamAI para uma única planta (síncrono).
        """
        relative_path = (planta.arquivo or "").strip()
        file_path = UPLOADS_PATH / relative_path
        
        if not file_path.exists():
            # Fallback para legado ou caminhos alternativos
            alt_path = Path("uploads") / relative_path
            if alt_path.exists():
                file_path = alt_path
            elif "/" not in relative_path and (UPLOADS_PATH / relative_path).exists():
                file_path = UPLOADS_PATH / relative_path
            else:
                raise FileNotFoundError(f"Arquivo DXF não encontrado em {file_path}")

        entity = EntityDxf(file_path)
        context_agent = create_context_agent()
        layer_agent = create_classificator_agent(tools=[]) 
        spatial_agent = create_spatial_analyst_agent(tools=[])
        surveyor_agent = create_surveyor_agent(tools=[])

        team = create_team(entity, [context_agent, layer_agent, spatial_agent, surveyor_agent])
        response = team.run(f"Analise a planta do tipo '{planta.tipo}' no arquivo '{planta.arquivo}'.")

        return response.content

    def save_results(self, project_id: int, results: list):
        """Salva os resultados em um arquivo JSON."""
        file_path = RESULTS_PATH / f"{project_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    def get_saved_results(self, project_id: int):
        """Recupera resultados salvos."""
        file_path = RESULTS_PATH / f"{project_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
