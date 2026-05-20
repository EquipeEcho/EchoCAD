#!/usr/bin/env python3
"""
Script de Teste - EchoCAD Excel Generation
Valida a integração de geração de Excel no pipeline
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Adiciona o caminho do módulo
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Testa se todos os imports necessários funcionam."""
    print("🧪 Testando imports...")
    try:
        from app.backend.src.modules.deprecated.entity_dxf import EntityDxf
        from app.backend.src.modules.deprecated.team_ai import create_team
        from app.backend.src.modules.deprecated.main import (
            run_extraction,
            _gerar_excel_a_partir_json,
        )
        from app.backend.src.modules.deprecated.tools.memorial_populator import (
            MemorialPopulator,
            run_population,
        )
        from app.backend.src.modules.deprecated.agents.agent_context import (
            create_context_agent,
        )
        from app.backend.src.modules.deprecated.agents.agent_layer_select import (
            create_classificator_agent,
        )
        from app.backend.src.modules.deprecated.agents.agent_spatial_analyst import (
            create_spatial_analyst_agent,
        )
        from app.backend.src.modules.deprecated.agents.agent_surveyor import (
            create_surveyor_agent,
        )

        print("✓ Todos os imports funcionam!")
        return True
    except ImportError as e:
        print(f"✗ Erro de import: {e}")
        return False


def test_template_exists():
    """Testa se o template Excel existe."""
    print("\n🧪 Testando existência do template...")
    template_path = (
        Path(__file__).parent.parent.parent / "templates" / "memorial_model.xlsx"
    )
    if template_path.exists():
        print(f"✓ Template encontrado: {template_path}")
        print(f"  Tamanho: {template_path.stat().st_size} bytes")
        return True
    else:
        print(f"✗ Template não encontrado: {template_path}")
        return False


def test_results_dir():
    """Testa se o diretório de resultados existe."""
    print("\n🧪 Testando diretório de resultados...")
    results_dir = Path(__file__).parent / "results"
    if results_dir.exists():
        print(f"✓ Diretório de resultados existe: {results_dir}")
        return True
    else:
        print(f"✗ Diretório não encontrado. Criando...")
        try:
            results_dir.mkdir(exist_ok=True)
            print(f"✓ Diretório criado com sucesso: {results_dir}")
            return True
        except Exception as e:
            print(f"✗ Erro ao criar diretório: {e}")
            return False


def test_memorial_populator():
    """Testa a classe MemorialPopulator com dados fictícios."""
    print("\n🧪 Testando MemorialPopulator...")
    try:
        from app.backend.src.modules.deprecated.tools.memorial_populator import (
            MemorialPopulator,
        )

        template_path = (
            Path(__file__).parent.parent.parent / "templates" / "memorial_model.xlsx"
        )
        output_path = Path(__file__).parent / "results" / "test_memorial.xlsx"

        if not template_path.exists():
            print(f"✗ Template não encontrado: {template_path}")
            return False

        # Testa instanciação
        populator = MemorialPopulator(str(template_path), str(output_path))
        print(f"✓ MemorialPopulator instanciado com sucesso")

        # Testa com dados fictícios
        test_data = {
            "arq-alvenaria": {
                "LINE": {"total_length": 45.5},
                "LWPOLYLINE": {"total_length": 12.3},
            },
            "arq-parede": {"LINE": {"total_length": 28.7}},
        }

        try:
            populator.populate_alvenaria(test_data)
            populator.add_metadata("alvenaria", "Teste automatizado")
            populator.save()
            print(f"✓ Excel de teste gerado: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Erro ao popular Excel: {e}")
            return False

    except ImportError as e:
        print(f"✗ Erro de import: {e}")
        return False


def test_json_parsing():
    """Testa parsing de JSON."""
    print("\n🧪 Testando parsing de JSON...")

    test_json = json.dumps(
        {
            "resumo_executivo": {
                "arq-alvenaria": {
                    "LINE": {"total_length": 50},
                    "LWPOLYLINE": {"total_length": 15},
                }
            },
            "sintese": "Resultado do levantamento de alvenaria",
        }
    )

    try:
        dados = json.loads(test_json)
        print(f"✓ JSON parsing funciona corretamente")
        print(f"  Chaves: {list(dados.keys())}")
        return True
    except Exception as e:
        print(f"✗ Erro ao fazer parse: {e}")
        return False


def test_discipline_detection():
    """Testa detecção automática de disciplina."""
    print("\n🧪 Testando detecção automática de disciplina...")

    test_cases = [
        ("preciso do levantamento de ALVENARIA", "alvenaria"),
        ("quantas PAREDES tem no projeto?", "alvenaria"),
        ("levantamento de circuitos ELÉTRICOS", "eletrica"),
        ("quanto de ÁGUA e esgoto?", "hidraulica"),
        ("comprimento de cabo de REDE", "rede"),
    ]

    all_passed = True
    for prompt, expected_discipline in test_cases:
        prompt_lower = prompt.lower()
        detected = "indefinido"

        if any(word in prompt_lower for word in ["parede", "alvenaria", "alv", "arq"]):
            detected = "alvenaria"
        elif any(
            word in prompt_lower
            for word in ["elétric", "elet", "fio", "circuito", "luz"]
        ):
            detected = "eletrica"
        elif any(
            word in prompt_lower
            for word in ["hidráulic", "hid", "água", "cano", "esgoto"]
        ):
            detected = "hidraulica"
        elif any(word in prompt_lower for word in ["rede", "dados", "telefone", "net"]):
            detected = "rede"

        status = "✓" if detected == expected_discipline else "✗"
        print(
            f"{status} '{prompt[:30]}...' → {detected} (esperado: {expected_discipline})"
        )

        if detected != expected_discipline:
            all_passed = False

    return all_passed


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("🧪 SUITE DE TESTES - EchoCAD Excel Generation")
    print(f"   Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    results = {
        "imports": test_imports(),
        "template": test_template_exists(),
        "results_dir": test_results_dir(),
        "json_parsing": test_json_parsing(),
        "discipline_detection": test_discipline_detection(),
        "memorial_populator": test_memorial_populator(),
    }

    print("\n" + "=" * 60)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{status:12} | {test_name}")

    print("=" * 60)
    print(f"Total: {passed}/{total} testes passaram")

    if passed == total:
        print("\n🎉 Todos os testes passaram! Sistema pronto para uso.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique acima.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
