import sys
from pathlib import Path

# Adiciona o diretório atual ao sys.path para importações funcionarem
sys.path.append(str(Path(__file__).parent))

from src.modules.ai_orchestrator import AIOrchestrator
from src.models.projeto_db import Planta

class MockDB:
    def query(self, *args, **kwargs):
        return self
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return None

def test_pipeline():
    print("Iniciando teste do pipeline de IA...")
    
    # Criar um objeto Planta fictício
    # Note: O arquivo deve existir em backend/uploads/teste.dxf
    planta = Planta(
        tipo="Alvenaria",
        arquivo="teste.dxf",
        id_projeto=999
    )
    
    # Instanciar orquestrador com DB mockado (não vamos usar o run_analysis_for_project que depende do DB)
    orchestrator = AIOrchestrator(db=MockDB())
    
    try:
        print(f"Analisando planta: {planta.arquivo} do tipo {planta.tipo}")
        resultado = orchestrator.analyze_planta(planta)
        
        print("\n=== RESULTADO DA IA ===")
        print(resultado)
        print("=======================\n")
        
        # Salvar manualmente para simular o comportamento real
        orchestrator.save_results(999, [{"planta_id": 1, "arquivo": planta.arquivo, "resultado": resultado}])
        print("Resultado salvo em results/999.json")
        
    except Exception as e:
        print(f"ERRO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pipeline()
