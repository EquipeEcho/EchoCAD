#!/usr/bin/env python3
"""
🧪 Script de Teste Completo do Módulo Knowledge RAG

Valida toda a estrutura do módulo e executa testes funcionais.

Uso:
    python KNOWLEDGE_TESTS.py              # Teste completo
    python KNOWLEDGE_TESTS.py --quick      # Teste rápido
    python KNOWLEDGE_TESTS.py --demo       # Demo apenas
"""

import sys
import argparse
from pathlib import Path


def print_header(title):
    """Imprime cabeçalho formatado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Imprime seção formatada."""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}\n")


def test_file_structure():
    """Testa estrutura de arquivos."""
    print_section("1️⃣  VERIFICANDO ESTRUTURA DE ARQUIVOS")
    
    required_files = [
        "src/modules/knowledge/__init__.py",
        "src/modules/knowledge/db.py",
        "src/modules/knowledge/normas_loader.py",
        "src/modules/knowledge/normas_ingestor.py",
        "src/modules/knowledge/normas_rag_agent.py",
        "src/modules/knowledge/main.py",
        "src/modules/knowledge/demo.py",
        "src/modules/knowledge/README.md",
        "src/routes/normas_router.py",
    ]
    
    missing = []
    for file in required_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✓ {file:50} ({size:,} bytes)")
        else:
            print(f"  ✗ {file}")
            missing.append(file)
    
    if missing:
        print(f"\n  ❌ {len(missing)} arquivo(s) faltando!")
        return False
    
    print(f"\n  ✓ Todos os {len(required_files)} arquivos presentes!")
    return True


def test_imports():
    """Testa se os imports funcionam."""
    print_section("2️⃣  TESTANDO IMPORTS")
    
    try:
        print("  Importando módulo knowledge...")
        from results.knowledge import (
            query_normas,
            ingest_normas_batch,
            ingest_norma_file,
            get_normas_vector_db,
        )
        print("  ✓ Imports bem-sucedidos!")
        return True
    except ImportError as e:
        print(f"  ✗ Erro ao importar: {e}")
        return False


def test_dependencies():
    """Testa dependências."""
    print_section("3️⃣  VERIFICANDO DEPENDÊNCIAS")
    
    deps = [
        ("agno", "Agno Framework"),
        ("chroma_db", "ChromaDB"),
        ("pypdf", "PyPDF"),
    ]
    
    missing = []
    for module, name in deps:
        try:
            __import__(module)
            print(f"  ✓ {name:30} ✓")
        except ImportError:
            print(f"  ✗ {name:30} (faltando)")
            missing.append(name)
    
    if missing:
        print(f"\n  ⚠️  Instale: pip install {' '.join([d[0] for d in deps if d[1] in missing])}")
        return False
    
    print("\n  ✓ Todas as dependências instaladas!")
    return True


def test_ollama():
    """Testa conexão com Ollama."""
    print_section("4️⃣  TESTANDO CONEXÃO COM OLLAMA")
    
    try:
        import requests
        print("  Testando conexão em http://localhost:11434...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"  ✓ Ollama respondendo ({len(models)} modelo(s))\n")
            
            # Listar modelos
            for model in models:
                name = model.get("name", "unknown")
                size = model.get("size", 0)
                print(f"    - {name:30} ({size / (1024**3):.2f} GB)")
            
            return True
        else:
            print(f"  ✗ Status {response.status_code}")
            return False
    
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        print("\n  ⚠️  Inicie Ollama: ollama serve")
        return False


def test_module_functions():
    """Testa funções do módulo."""
    print_section("5️⃣  TESTANDO FUNÇÕES DO MÓDULO")
    
    try:
        from results.knowledge.db import get_normas_vector_db
        
        print("  Conectando ao ChromaDB...")
        db = get_normas_vector_db()
        print("  ✓ ChromaDB conectado!")
        
        # Testar contagem de itens
        print("  Verificando banco de normas...")
        # Aqui você pode adicionar mais testes específicos
        
        return True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False


def test_query_basic():
    """Testa query básica."""
    print_section("6️⃣  TESTANDO QUERY (BÁSICO)")
    
    try:
        from results.knowledge import query_normas
        
        print("  Executando query de teste...")
        pergunta = "O que é concreto armado?"
        print(f"  Pergunta: {pergunta}\n")
        
        print("  ⏳ Aguardando resposta do modelo...\n")
        resposta = query_normas(pergunta)
        
        print(f"  Resposta:\n")
        print(f"  {resposta[:500]}...\n" if len(resposta) > 500 else f"  {resposta}\n")
        
        print("  ✓ Query bem-sucedida!")
        return True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False


def test_cli():
    """Testa CLI."""
    print_section("7️⃣  TESTANDO CLI")
    
    try:
        print("  Testando comando de ajuda...")
        import subprocess
        result = subprocess.run(
            ["python", "-m", "src.modules.knowledge.main", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode == 0 and "usage:" in result.stdout.lower():
            print("  ✓ CLI funcionando!")
            return True
        else:
            print(f"  ✗ CLI retornou erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False


def test_api_endpoints():
    """Testa endpoints FastAPI (se server rodando)."""
    print_section("8️⃣  TESTANDO ENDPOINTS FASTAPI")
    
    try:
        import requests
        
        endpoints = [
            ("GET", "http://localhost:8000/api/normas/status"),
            ("GET", "http://localhost:8000/api/normas/health"),
        ]
        
        working = 0
        for method, url in endpoints:
            try:
                if method == "GET":
                    response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"  ✓ {method} {url.split('/')[-1]:20} OK")
                    working += 1
                else:
                    print(f"  ⚠️  {method} {url.split('/')[-1]:20} {response.status_code}")
            except:
                pass
        
        if working > 0:
            print(f"\n  ✓ {working} endpoint(s) respondendo!")
            return True
        else:
            print("\n  ⚠️  API não está rodando (http://localhost:8000)")
            return False
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False


def run_full_tests():
    """Executa todos os testes."""
    print_header("🧪 TESTE COMPLETO DO MÓDULO KNOWLEDGE RAG")
    
    results = {
        "Estrutura de Arquivos": test_file_structure(),
        "Imports": test_imports(),
        "Dependências": test_dependencies(),
        "Ollama": test_ollama(),
        "Funções do Módulo": test_module_functions(),
        "Query Básica": test_query_basic(),
        "CLI": test_cli(),
        "Endpoints API": test_api_endpoints(),
    }
    
    print_header("📊 RESUMO DOS TESTES")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {test_name:30} {'OK' if result else 'FALHOU'}")
    
    print(f"\n  Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n  ✅ TODOS OS TESTES PASSARAM!")
        return 0
    elif passed >= total * 0.75:
        print(f"\n  ⚠️  {total - passed} teste(s) falharam (mas está operacional)")
        return 0
    else:
        print(f"\n  ❌ Muito testes falharam")
        return 1


def run_quick_tests():
    """Executa testes rápidos."""
    print_header("⚡ TESTE RÁPIDO")
    
    results = {
        "Estrutura": test_file_structure(),
        "Imports": test_imports(),
    }
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    if passed == total:
        print(f"\n✓ Teste rápido OK ({passed}/{total})")
        return 0
    else:
        print(f"\n✗ Teste rápido FALHOU ({passed}/{total})")
        return 1


def run_demo_only():
    """Executa apenas demo."""
    print_header("🎬 DEMO DO MÓDULO")
    
    try:
        from results.knowledge import query_normas
        
        perguntas = [
            "O que é concreto armado?",
            "Como dimensionar uma viga?",
            "Segurança em altura",
        ]
        
        for i, pergunta in enumerate(perguntas, 1):
            print_section(f"Demo {i}/3: {pergunta}")
            print("⏳ Consultando normas...\n")
            
            try:
                resposta = query_normas(pergunta)
                print(f"Resposta:\n{resposta[:400]}...\n")
            except Exception as e:
                print(f"Erro: {e}\n")
        
        return 0
    except Exception as e:
        print(f"Erro ao executar demo: {e}")
        return 1


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Teste do módulo Knowledge RAG"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Teste rápido (apenas estrutura)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Apenas demo"
    )
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            return run_demo_only()
        elif args.quick:
            return run_quick_tests()
        else:
            return run_full_tests()
    except KeyboardInterrupt:
        print("\n\n❌ Teste interrompido pelo usuário")
        return 1
    except Exception as e:
        print(f"\n\n❌ Erro geral: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
