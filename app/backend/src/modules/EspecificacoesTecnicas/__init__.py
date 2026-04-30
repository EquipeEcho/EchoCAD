# __init__.py
# Módulo de Especificações Técnicas do EchoCAD.
# Orquestra: extração de contexto do DXF → geração via IA → exportação DOCX.

import logging
import os
from pathlib import Path
from typing import Optional

from .dxf_context_extractor import DXFContextExtractor, ContextoDXF
from .spec_generator import SpecGenerator
from .docx_builder import build_docx

logger = logging.getLogger(__name__)


def gerar_especificacoes(
    dxf_file: str,
    output_path: str,
    nome_projeto: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Path:
    """
    Pipeline completo de geração de especificações técnicas.

    Args:
        dxf_file:     Caminho para o arquivo .dxf da planta.
        output_path:  Caminho de saída do .docx gerado.
        nome_projeto: Nome do projeto (opcional; inferido do arquivo se omitido).
        api_key:      Chave da API Claude (opcional; usa variável de ambiente se omitida).

    Returns:
        Path do arquivo .docx gerado.
    """
    logger.info(f"[EspecificacoesTecnicas] Iniciando: {os.path.basename(dxf_file)}")

    # 1. Extrair contexto do DXF
    nome = nome_projeto or Path(dxf_file).stem.replace('_', ' ').replace('-', ' ').title()
    extractor = DXFContextExtractor(dxf_file, nome_projeto=nome)
    ctx: ContextoDXF = extractor.extrair()

    logger.info(
        f"  Contexto: {len(ctx.ambientes)} ambientes | "
        f"{len(ctx.disciplinas)} disciplinas | "
        f"área total: {ctx.area_total}m²"
    )

    # 2. Gerar especificações via IA
    key = os.getenv("GROQ_API_KEY")
    generator = SpecGenerator(api_key=key)
    specs = generator.gerar(ctx)

    logger.info(f"  Especificações: {len(specs.secoes)} seções geradas")

    # 3. Exportar para DOCX
    arquivo_final = build_docx(specs, output_path)
    logger.info(f"  Documento gerado: {arquivo_final}")

    return arquivo_final


__all__ = [
    "gerar_especificacoes",
    "DXFContextExtractor",
    "ContextoDXF",
    "SpecGenerator",
    "build_docx",
]