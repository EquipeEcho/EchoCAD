#!/usr/bin/env python3
"""
test_especificacoes.py
======================
Script de teste standalone para o módulo de Especificações Técnicas.
Não depende do FastAPI nem do banco de dados — roda direto.

Uso (a partir de QUALQUER pasta):
    python test_especificacoes.py caminho/para/arquivo.dxf

Exemplos:
    # A partir da raiz do projeto
    python test_especificacoes.py app/backend/uploads/teste.dxf

    # A partir da pasta do módulo
    python app\\backend\\src\\modules\\EspecificacoesTecnicas\\test_especificacoes.py app\\backend\\uploads\\teste.dxf

Saídas geradas na pasta ./output_teste/:
    - contexto.json          -> dados extraídos do DXF (confira antes de chamar a IA)
    - especificacoes.docx    -> caderno completo gerado pela IA
"""

import importlib.util
import json
import logging
import os
import sys
from pathlib import Path

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("test_especificacoes")


# ── Localizar a pasta do módulo de qualquer ponto ───────────────────────────
def _encontrar_pasta_modulo() -> Path:
    """
    Procura EspecificacoesTecnicas subindo a partir deste script
    e a partir do diretório de trabalho atual.
    """
    script_dir = Path(__file__).resolve().parent
    cwd = Path.cwd().resolve()

    candidatos = [
        # O próprio diretório do script (se test_especificacoes.py estiver dentro do módulo)
        script_dir,
        # Caminhos relativos ao CWD (raiz do projeto)
        cwd / "app" / "backend" / "src" / "modules" / "EspecificacoesTecnicas",
        cwd / "src" / "modules" / "EspecificacoesTecnicas",
        cwd / "modules" / "EspecificacoesTecnicas",
        cwd / "EspecificacoesTecnicas",
        # Relativo ao diretório do script subindo níveis
        script_dir.parent / "EspecificacoesTecnicas",
        script_dir.parent.parent / "EspecificacoesTecnicas",
        script_dir.parent.parent.parent.parent
        / "src"
        / "modules"
        / "EspecificacoesTecnicas",
    ]

    for c in candidatos:
        if (
            c.is_dir()
            and (c / "__init__.py").exists()
            and (c / "dxf_context_extractor.py").exists()
        ):
            return c
    raise FileNotFoundError(
        "Pasta EspecificacoesTecnicas não encontrada. "
        "Execute o teste a partir da raiz do projeto."
    )


def _importar_arquivo(nome_modulo: str, caminho: Path):
    """Importa um .py diretamente pelo caminho, sem precisar de sys.path."""
    spec = importlib.util.spec_from_file_location(nome_modulo, str(caminho))
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível carregar o módulo '{nome_modulo}' de {caminho}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome_modulo] = mod
    spec.loader.exec_module(mod)
    return mod


def _carregar_modulo(pasta: Path):
    """
    Carrega o pacote EspecificacoesTecnicas pelos arquivos físicos,
    sem depender de sys.path ou estrutura de pacotes.
    """
    pkg = "EspecTec"  # nome curto para não conflitar com imports do projeto

    # Ordem importa: cada arquivo depende do anterior
    dxf_mod = _importar_arquivo(
        f"{pkg}.dxf_context_extractor", pasta / "dxf_context_extractor.py"
    )
    spec_mod = _importar_arquivo(f"{pkg}.spec_generator", pasta / "spec_generator.py")
    docx_mod = _importar_arquivo(f"{pkg}.docx_builder", pasta / "docx_builder.py")
    init_mod = _importar_arquivo(pkg, pasta / "__init__.py")

    return init_mod, dxf_mod


# ── Localizar e carregar ──────────────────────────────────────────────────────
pasta_modulo = _encontrar_pasta_modulo()

if pasta_modulo is None:
    logger.error(
        "Nao foi possivel encontrar o modulo EspecificacoesTecnicas.\n"
        "Certifique-se de que os 4 arquivos existem em:\n"
        "  app/backend/src/modules/EspecificacoesTecnicas/\n"
        "    __init__.py\n"
        "    dxf_context_extractor.py\n"
        "    spec_generator.py\n"
        "    docx_builder.py\n"
    )
    sys.exit(1)

logger.info(f"Modulo encontrado em: {pasta_modulo}")

try:
    _init, _dxf = _carregar_modulo(pasta_modulo)
    gerar_especificacoes = _init.gerar_especificacoes
    DXFContextExtractor = _dxf.DXFContextExtractor
except Exception as e:
    logger.error(f"Erro ao carregar modulo: {e}", exc_info=True)
    sys.exit(1)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Arquivo DXF
    if len(sys.argv) >= 2:
        dxf_path = Path(sys.argv[1])
    else:
        # Tentar encontrar o teste.dxf automaticamente
        tentativas = [
            Path.cwd() / "app" / "backend" / "uploads" / "teste.dxf",
            Path.cwd()
            / "app"
            / "backend"
            / "src"
            / "modules"
            / "Memorial"
            / "teste.dxf",
            pasta_modulo.parent / "Memorial" / "teste.dxf",
        ]
        dxf_path = next((p for p in tentativas if p.exists()), None)
        if dxf_path is None:
            print(__doc__)
            logger.error("Informe o caminho do arquivo DXF como argumento.")
            sys.exit(1)
        logger.info(f"Usando DXF padrao: {dxf_path}")

    dxf_path = Path(dxf_path).resolve()
    if not dxf_path.exists():
        logger.error(f"Arquivo nao encontrado: {dxf_path}")
        sys.exit(1)

    # Saída sempre no CWD (onde o terminal está)
    output_dir = Path.cwd() / "output_teste"
    output_dir.mkdir(exist_ok=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ETAPA 1 — Extrair contexto do DXF
    # ══════════════════════════════════════════════════════════════════════════
    print()
    logger.info("=" * 60)
    logger.info("ETAPA 1: Extraindo contexto do DXF...")
    logger.info("=" * 60)

    nome_projeto = dxf_path.stem.replace("_", " ").replace("-", " ").title()
    extractor = DXFContextExtractor(str(dxf_path), nome_projeto=nome_projeto)
    ctx = extractor.extrair()
    ctx_dict = ctx.to_dict()

    # Salvar JSON para inspeção
    contexto_path = output_dir / "contexto.json"
    contexto_path.write_text(
        json.dumps(ctx_dict, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    sep = "-" * 60
    print(f"\n{sep}")
    print(f"  Projeto   : {ctx.nome_projeto}")
    print(f"  Area total: {ctx.area_total} m2")
    print(f"  Ambientes : {len(ctx.ambientes)}")
    print(f"  Disciplinas ({len(ctx.disciplinas)}):")
    for d in sorted(ctx.disciplinas):
        print(f"    - {d}")
    print(f"  Sistemas ({len(ctx.sistemas)}):")
    for s in sorted(ctx.sistemas):
        print(f"    - {s}")
    print(f"  Flags:")
    for k, v in ctx_dict["flags"].items():
        print(f"    {'[x]' if v else '[ ]'} {k}")
    esquadrias = list(ctx.esquadrias.keys())
    if esquadrias:
        print(f"  Esquadrias: {', '.join(esquadrias[:10])}")
    print(sep)
    print(f"  -> Contexto salvo em: {contexto_path}")
    print(f"{sep}\n")

    if len(ctx.ambientes) == 0:
        logger.warning(
            "Nenhum ambiente encontrado no DXF.\n"
            "  O extrator le MTEXTs das layers 'ARQ - Textos' e 'Arquitetonico - Textos'.\n"
            "  Verifique se essas layers existem no seu arquivo."
        )

    # ══════════════════════════════════════════════════════════════════════════
    # ETAPA 2 — Gerar especificações via IA
    # ══════════════════════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("ETAPA 2: Gerando especificacoes tecnicas via IA...")
    logger.info("(Pode levar alguns minutos - a IA gera cada secao separadamente)")
    logger.info("=" * 60)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    api_key = GROQ_API_KEY
    if not api_key:
        logger.error(
            "GROQ_API_KEY nao definida. Defina antes de rodar:\n"
            "\n"
            "  Windows PowerShell:\n"
            "    $env:GROQ_API_KEY = 'sk-ant-sua-chave-aqui'\n"
            "\n"
            "  Windows CMD:\n"
            "    set GROQ_API_KEY=sk-ant-sua-chave-aqui\n"
            "\n"
            "  Linux/macOS:\n"
            "    export GROQ_API_KEY='sk-ant-sua-chave-aqui'\n"
        )
        sys.exit(1)

    output_docx = output_dir / f"especificacoes_{dxf_path.stem}.docx"

    try:
        arquivo_gerado = gerar_especificacoes(
            dxf_file=str(dxf_path),
            output_path=str(output_docx),
            nome_projeto=nome_projeto,
            api_key=api_key,
        )

        print(f"\n{sep}")
        print(f"  Especificacoes geradas com sucesso!")
        print(f"  -> Arquivo: {arquivo_gerado}")
        print(f"{sep}\n")

    except Exception as e:
        logger.error(f"Erro ao gerar especificacoes: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
