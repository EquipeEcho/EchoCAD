# __init__.py
# Módulo de Especificações Técnicas do EchoCAD.
# Orquestra: extração de contexto do DXF → geração via IA → exportação DOCX.

import logging
import os
from pathlib import Path
from typing import Any, Optional

from src.exceptions import AIProviderException

from .dxf_context_extractor import (
    AmbienteInfo,
    DXFContextExtractor,
    ContextoDXF,
    EsquadriaInfo,
)
from .spec_generator import SpecGenerator
from .docx_builder import build_docx

logger = logging.getLogger(__name__)


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _enriquecer_contexto_com_drill(
    ctx: ContextoDXF, drill_data: Optional[dict[str, Any]]
) -> ContextoDXF:
    if not isinstance(drill_data, dict):
        return ctx

    resumo = drill_data.get("resumo_global") or {}
    paredes = drill_data.get("paredes") or []
    vigas = drill_data.get("vigas") or []
    colunas = drill_data.get("colunas") or []
    lajes = drill_data.get("laje") or []
    infraestrutura = drill_data.get("infraestrutura") or {}

    area_laje = sum(_to_float(item.get("area_m2")) for item in lajes)
    area_resumo = _to_float(resumo.get("area_total_laje_m2"))
    area_total = area_resumo or area_laje

    if ctx.area_total <= 0 and area_total > 0:
        ctx.area_total = round(area_total, 2)

    if not ctx.ambientes and ctx.area_total > 0:
        perimetro = sum(_to_float(parede.get("comprimento_m")) for parede in paredes)
        alturas = [
            _to_float(parede.get("altura_m"))
            for parede in paredes
            if _to_float(parede.get("altura_m")) > 0
        ]
        pe_direito = sum(alturas) / len(alturas) if alturas else 2.8
        ctx.ambientes.append(
            AmbienteInfo(
                nome="AMBIENTE TECNICO",
                subtitulo="Gerado pelos quantitativos do DXF",
                area=round(ctx.area_total, 2),
                perimetro=round(perimetro, 2),
                pe_direito=round(pe_direito, 2),
                uso="uso_geral",
            )
        )

    if paredes or _to_float(resumo.get("volume_final_liquido_alvenaria_m3")) > 0:
        ctx.disciplinas.add("alvenaria")

    if vigas or colunas or lajes:
        ctx.disciplinas.add("estrutura_concreto")

    eletrica = infraestrutura.get("eletrica") or []
    hidraulica = infraestrutura.get("hidraulica") or []
    if eletrica or _to_float(resumo.get("comprimento_total_fios_m")) > 0:
        ctx.disciplinas.add("instalações_elétricas")
        ctx.sistemas.add("instalações_elétricas")
        ctx.sistemas.add("iluminação")
    if hidraulica or _to_float(resumo.get("comprimento_total_canos_m")) > 0:
        ctx.disciplinas.add("hidráulica_água_fria")
        ctx.sistemas.add("louças_metais")

    quantidade_portas = int(_to_float(resumo.get("quantidade_total_portas")))
    quantidade_janelas = int(_to_float(resumo.get("quantidade_total_janelas")))
    if quantidade_portas or quantidade_janelas:
        ctx.disciplinas.add("esquadrias")
    if quantidade_portas and "PORTAS" not in ctx.esquadrias:
        ctx.esquadrias["PORTAS"] = EsquadriaInfo(
            codigo="PORTAS", tipo="Porta", quantidade=quantidade_portas
        )
    if quantidade_janelas and "JANELAS" not in ctx.esquadrias:
        ctx.esquadrias["JANELAS"] = EsquadriaInfo(
            codigo="JANELAS", tipo="Janela", quantidade=quantidade_janelas
        )

    ctx.tem_rede_dados = ctx.tem_rede_dados or "rede_lógica_cftv" in ctx.sistemas

    logger.info(
        "Contexto enriquecido pelo drill.py: "
        f"{len(ctx.ambientes)} ambientes | "
        f"{len(ctx.disciplinas)} disciplinas | "
        f"{len(ctx.sistemas)} sistemas | "
        f"area total: {ctx.area_total}m2"
    )
    return ctx


async def gerar_especificacoes(
    dxf_file: str,
    output_path: str,
    nome_projeto: Optional[str] = None,
    api_key: Optional[str] = None,
    drill_data: Optional[dict[str, Any]] = None,
    use_ollama: bool = False,
) -> Path:
    """
    Pipeline completo de geração de especificações técnicas.

    Args:
        dxf_file:     Caminho para o arquivo .dxf da planta.
        output_path:  Caminho de saída do .docx gerado.
        nome_projeto: Nome do projeto (opcional; inferido do arquivo se omitido).
        api_key:      Chave da API Groq (opcional; usa variável de ambiente se omitida).
        drill_data:   Dados extraídos do Drill (opcional).
        use_ollama:   Preferência do usuário (True=Ollama, False=Groq).

    Returns:
        Path do arquivo .docx gerado.
    
    Raises:
        NoGroqTokenException: Sem token Groq configurado
        OllamaUnavailableException: Ollama não está respondendo
        GroqQuotaExceededException: Limite de uso Groq atingido
        NoValidProviderException: Nenhum provedor disponível
    """
    logger.info(
        f"[EspecificacoesTecnicas] Iniciando: {os.path.basename(dxf_file)} "
        f"(preferência: {'Ollama' if use_ollama else 'Groq'})"
    )

    try:
        # 1. Extrair contexto do DXF
        nome = (
            nome_projeto or Path(dxf_file).stem.replace("_", " ").replace("-", " ").title()
        )
        extractor = DXFContextExtractor(dxf_file, nome_projeto=nome)
        ctx: ContextoDXF = extractor.extrair()
        ctx = _enriquecer_contexto_com_drill(ctx, drill_data)

        logger.info(
            f"  Contexto: {len(ctx.ambientes)} ambientes | "
            f"{len(ctx.disciplinas)} disciplinas | "
            f"área total: {ctx.area_total}m²"
        )

        # 2. Gerar especificações via IA
        generator = SpecGenerator(api_key=api_key, use_ollama=use_ollama)
        
        # Auto-select do provedor com fallback automático
        await generator.auto_select_provider()
        logger.info(f"  Provedor selecionado: {generator.provider}")
        
        specs = await generator.gerar(ctx)

        logger.info(f"  Especificações: {len(specs.secoes)} seções geradas")

        # 3. Exportar para DOCX
        arquivo_final = build_docx(specs, output_path)
        logger.info(f"  Documento gerado: {arquivo_final}")

        return arquivo_final
    
    except AIProviderException as e:
        logger.error(f"Erro de provedor de IA: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar especificações: {e}", exc_info=True)
        raise


__all__ = [
    "gerar_especificacoes",
    "DXFContextExtractor",
    "ContextoDXF",
    "SpecGenerator",
    "build_docx",
]
