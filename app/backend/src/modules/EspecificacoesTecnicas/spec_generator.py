# spec_generator.py
# Gera as especificações técnicas usando a API do Claude (claude-sonnet-4-20250514).
# Recebe o contexto extraído do DXF e o modelo de especificações, e produz
# um documento Word (.docx) estruturado seguindo o padrão do Exército.

import json
import logging
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import requests

from .dxf_context_extractor import ContextoDXF

logger = logging.getLogger(__name__)

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL   = "claude-sonnet-4-20250514"
MAX_TOKENS     = 8000


# ---------------------------------------------------------------------------
# Prompt de sistema
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = textwrap.dedent("""
Você é um engenheiro civil especialista em elaboração de cadernos de encargos
e especificações técnicas para obras militares do Exército Brasileiro.

Você redige textos técnicos precisos, formais e completos, seguindo as normas
da ABNT, o padrão do Comando de Engenharia do Exército e as boas práticas de
construção civil brasileira.

Ao gerar especificações técnicas:
- Use linguagem formal e técnica.
- Referencie normas ABNT pertinentes (NBR).
- Descreva materiais, processos executivos e critérios de aceitação.
- Organize em seções numeradas conforme o modelo fornecido.
- Para cada seção, inclua: Objetivo, Referências Normativas, Materiais,
  Execução e Critérios de Aceitação/Medição.
- Adapte o conteúdo ao contexto real extraído da planta (ambientes, sistemas,
  disciplinas presentes).
- Não invente sistemas que não foram identificados na planta.
- Responda APENAS com JSON válido, sem markdown, sem explicações.
""").strip()


# ---------------------------------------------------------------------------
# Dataclass de resultado
# ---------------------------------------------------------------------------
@dataclass
class SecaoEspec:
    numero: str
    titulo: str
    conteudo: str
    subsecoes: List['SecaoEspec'] = None

    def __post_init__(self):
        if self.subsecoes is None:
            self.subsecoes = []


@dataclass
class EspecificacoesTecnicas:
    nome_projeto: str
    numero_protocolo: str
    objeto: str
    secoes: List[SecaoEspec]
    referencias_normativas: List[str]
    vida_util: List[Dict]


# ---------------------------------------------------------------------------
# Gerador principal
# ---------------------------------------------------------------------------
class SpecGenerator:

    def __init__(self, api_key: Optional[str] = None):
        # A key é injetada pelo runtime do claude.ai — não precisa ser
        # passada explicitamente quando rodando dentro dos artefatos.
        self._api_key = api_key

    def _chamar_api(self, messages: List[Dict], max_tokens: int = MAX_TOKENS) -> Optional[str]:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["x-api-key"] = self._api_key

        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": max_tokens,
            "system": SYSTEM_PROMPT,
            "messages": messages,
        }

        try:
            resp = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            # Extrair texto da resposta
            for block in data.get("content", []):
                if block.get("type") == "text":
                    return block["text"]
        except Exception as e:
            logger.error(f"Erro na API Claude: {e}")
        return None

    @staticmethod
    def _extrair_json(texto: str) -> Optional[dict]:
        """Extrai JSON da resposta, tolerando marcadores de bloco."""
        if not texto:
            return None
        # Remover blocos de código
        limpo = re.sub(r'```(?:json)?', '', texto).strip()
        # Tentar parse direto
        try:
            return json.loads(limpo)
        except Exception:
            pass
        # Tentar encontrar primeiro objeto JSON
        m = re.search(r'\{.*\}', limpo, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return None

    # ------------------------------------------------------------------
    # Gerar objeto e contexto
    # ------------------------------------------------------------------
    def _gerar_objeto_e_contexto(self, ctx: ContextoDXF) -> Dict:
        """Gera o texto de objeto, finalidade e concepção do projeto."""
        ambientes_resumo = [
            f"{a.nome}{' (' + a.subtitulo + ')' if a.subtitulo else ''}: "
            f"{a.area}m² | P={a.perimetro}m | PD={a.pe_direito}m"
            for a in ctx.ambientes[:30]
        ]

        prompt = f"""
Com base no seguinte contexto extraído da planta CAD do projeto, gere os textos
de abertura do caderno de especificações técnicas.

CONTEXTO DO PROJETO:
- Nome: {ctx.nome_projeto}
- Área total: {ctx.area_total}m²
- Disciplinas identificadas: {', '.join(sorted(ctx.disciplinas))}
- Sistemas identificados: {', '.join(sorted(ctx.sistemas))}
- Ambientes principais:
{chr(10).join('  • ' + a for a in ambientes_resumo)}

Retorne APENAS um JSON com esta estrutura:
{{
  "numero_protocolo": "a ser definido",
  "objeto": "texto descrevendo o objeto da obra (2-4 frases)",
  "finalidade": "texto descrevendo a finalidade (2-3 frases)",
  "concepcao": "texto descrevendo a concepção do projeto (3-5 frases)"
}}
"""
        resposta = self._chamar_api([{"role": "user", "content": prompt}], max_tokens=1000)
        dados = self._extrair_json(resposta)
        if not dados:
            return {
                "numero_protocolo": "XXX",
                "objeto": f"Execução de obras de construção e reforma nas instalações do projeto {ctx.nome_projeto}.",
                "finalidade": "As presentes especificações técnicas têm por finalidade descrever os serviços a serem executados pela contratada.",
                "concepcao": f"O projeto compreende a construção e adequação de ambientes com área total de {ctx.area_total}m²."
            }
        return dados

    # ------------------------------------------------------------------
    # Gerar seção por disciplina
    # ------------------------------------------------------------------
    def _gerar_secao_disciplina(
        self,
        ctx: ContextoDXF,
        numero: str,
        titulo: str,
        disciplina: str,
        instrucoes_extra: str = ''
    ) -> Optional[SecaoEspec]:
        """Gera uma seção completa de especificações para uma disciplina."""

        # Filtrar ambientes relevantes para essa disciplina
        ambientes_relevantes = []
        if disciplina == 'alvenaria':
            ambientes_relevantes = [
                a for a in ctx.ambientes
                if a.uso not in ('área_externa', 'cobertura')
            ][:15]
        elif disciplina == 'esquadrias':
            ambientes_relevantes = ctx.ambientes[:10]
        elif disciplina == 'hidráulica':
            ambientes_relevantes = [
                a for a in ctx.ambientes
                if a.uso in ('sanitário', 'área_alimentação')
            ][:10]
        else:
            ambientes_relevantes = ctx.ambientes[:8]

        amb_texto = '\n'.join(
            f"  • {a.nome}: {a.area}m², PD={a.pe_direito}m"
            for a in ambientes_relevantes
        ) or "  • Conforme projeto"

        esquadrias_texto = ''
        if ctx.esquadrias and disciplina == 'esquadrias':
            esquadrias_texto = '\nEsquadrias identificadas:\n' + '\n'.join(
                f"  • {k}: {v.tipo} ({v.quantidade} unidades)"
                for k, v in list(ctx.esquadrias.items())[:10]
            )

        sistemas_relevantes = [s for s in ctx.sistemas if disciplina.split('_')[0] in s.lower()]
        sistemas_texto = ', '.join(sistemas_relevantes) if sistemas_relevantes else ''

        prompt = f"""
Gere a seção "{numero}. {titulo}" do caderno de especificações técnicas.

CONTEXTO:
- Projeto: {ctx.nome_projeto}
- Área total: {ctx.area_total}m²
- Ambientes que receberão este serviço:
{amb_texto}{esquadrias_texto}
- Sistemas detectados nesta disciplina: {sistemas_texto or 'conforme projeto'}
{instrucoes_extra}

ESTRUTURA OBRIGATÓRIA para cada subseção:
- Referências normativas (liste NBRs pertinentes)
- Materiais (especificações técnicas dos materiais)
- Execução (passo a passo do processo construtivo)
- Critérios de aceitação e medição

Retorne APENAS um JSON com esta estrutura:
{{
  "numero": "{numero}",
  "titulo": "{titulo}",
  "introducao": "texto introdutório da seção (2-4 frases)",
  "subsecoes": [
    {{
      "numero": "{numero}.1",
      "titulo": "título da subseção",
      "referencias_normativas": ["NBR XXXXX - ...", "..."],
      "materiais": "especificação detalhada dos materiais",
      "execucao": "descrição detalhada do processo executivo",
      "criterios": "critérios de aceitação e forma de medição"
    }}
  ]
}}
"""
        resposta = self._chamar_api([{"role": "user", "content": prompt}], max_tokens=2500)
        dados = self._extrair_json(resposta)
        if not dados:
            logger.warning(f"Falha ao gerar seção {numero} - {titulo}")
            return None

        subsecoes = []
        for sub in dados.get('subsecoes', []):
            conteudo_parts = []
            if sub.get('referencias_normativas'):
                refs = sub['referencias_normativas']
                conteudo_parts.append(
                    "**Referências Normativas:**\n" +
                    '\n'.join(f"- {r}" for r in refs)
                )
            if sub.get('materiais'):
                conteudo_parts.append(f"**Materiais:**\n{sub['materiais']}")
            if sub.get('execucao'):
                conteudo_parts.append(f"**Execução:**\n{sub['execucao']}")
            if sub.get('criterios'):
                conteudo_parts.append(f"**Critérios de Aceitação:**\n{sub['criterios']}")

            subsecoes.append(SecaoEspec(
                numero=sub.get('numero', ''),
                titulo=sub.get('titulo', ''),
                conteudo='\n\n'.join(conteudo_parts),
            ))

        return SecaoEspec(
            numero=numero,
            titulo=titulo,
            conteudo=dados.get('introducao', ''),
            subsecoes=subsecoes,
        )

    # ------------------------------------------------------------------
    # Gerar referências normativas e vida útil
    # ------------------------------------------------------------------
    def _gerar_referencias_e_vida_util(self, ctx: ContextoDXF) -> Dict:
        disciplinas_str = ', '.join(sorted(ctx.disciplinas))
        sistemas_str = ', '.join(sorted(ctx.sistemas))

        prompt = f"""
Para um projeto com as seguintes disciplinas e sistemas:
- Disciplinas: {disciplinas_str}
- Sistemas: {sistemas_str}

Gere:
1. Lista completa de referências normativas ABNT (NBRs) pertinentes.
2. Tabela de vida útil e garantias dos principais itens.

Retorne APENAS JSON:
{{
  "referencias_normativas": [
    "ABNT NBR XXXXX - Título da norma",
    "..."
  ],
  "vida_util": [
    {{
      "item": "Nome do item",
      "vida_util_anos": "X a Y",
      "garantia_anos": "Z",
      "nbr": "XXXXX; YYYYY"
    }}
  ]
}}
"""
        resposta = self._chamar_api([{"role": "user", "content": prompt}], max_tokens=1500)
        dados = self._extrair_json(resposta)
        if not dados:
            return {
                "referencias_normativas": [
                    "ABNT NBR 5671 - Participação dos intervenientes em serviços e obras de engenharia e arquitetura.",
                    "ABNT NBR 7678 - Segurança na execução de obras e serviços de construção.",
                    "ABNT NBR 13531 - Elaboração de projetos de edificações – Atividades técnicas.",
                ],
                "vida_util": []
            }
        return dados

    # ------------------------------------------------------------------
    # Orquestrador principal
    # ------------------------------------------------------------------
    def gerar(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        logger.info(f"Iniciando geração de specs para: {ctx.nome_projeto}")

        # 1. Objeto e contexto geral
        abertura = self._gerar_objeto_e_contexto(ctx)

        # 2. Referências normativas e vida útil
        refs_vida = self._gerar_referencias_e_vida_util(ctx)

        # 3. Definir quais seções gerar com base nas disciplinas/sistemas
        secoes_map = self._mapear_secoes(ctx)

        # 4. Gerar cada seção
        secoes: List[SecaoEspec] = []
        for num, titulo, disciplina, extra in secoes_map:
            logger.info(f"Gerando seção {num}: {titulo}...")
            secao = self._gerar_secao_disciplina(ctx, num, titulo, disciplina, extra)
            if secao:
                secoes.append(secao)

        return EspecificacoesTecnicas(
            nome_projeto=ctx.nome_projeto,
            numero_protocolo=abertura.get('numero_protocolo', 'XXX'),
            objeto=abertura.get('objeto', ''),
            secoes=secoes,
            referencias_normativas=refs_vida.get('referencias_normativas', []),
            vida_util=refs_vida.get('vida_util', []),
        )

    def _mapear_secoes(self, ctx: ContextoDXF) -> List[tuple]:
        """Retorna a lista de seções a gerar, filtrando pelo contexto da planta."""
        secoes = []
        num = 1

        # Serviços Técnicos e Preliminares — sempre presentes
        secoes.append((str(num), "SERVIÇOS TÉCNICOS", "tecnico",
                        "Inclua: Elaboração de Projetos Executivos, ART, mão de obra especializada."))
        num += 1

        secoes.append((str(num), "SERVIÇOS PRELIMINARES", "preliminar",
                        "Inclua: limpeza inicial, topografia, sondagem, canteiro de obras, demolições."))
        num += 1

        # Somente se houver movimentação de solo ou escavação
        if any('fundações' in d or 'escavação' in d.lower() for d in ctx.disciplinas):
            secoes.append((str(num), "MOVIMENTO DE SOLO", "movimento_solo",
                            "Inclua: escavações, aterros, nivelamentos e compactações."))
            num += 1

        # Estrutura — gerar se houver qualquer disciplina estrutural
        tem_estrutura = any(d in ctx.disciplinas for d in
                            ['estrutura_concreto', 'fundações', 'estrutura_cobertura'])
        if tem_estrutura or ctx.tem_estrutura_metalica:
            extra = ""
            if ctx.tem_estrutura_metalica:
                extra += " O projeto possui estruturas metálicas identificadas nas plantas."
            if 'estrutura_cobertura' in ctx.disciplinas:
                extra += " Há estrutura de cobertura a ser executada."
            secoes.append((str(num), "SISTEMAS ESTRUTURAIS", "estrutura", extra))
            num += 1

        # Alvenarias — sempre presente
        secoes.append((str(num), "ALVENARIAS", "alvenaria",
                        f"O projeto tem drywall: {ctx.tem_drywall}. "
                        "Inclua painéis em alvenaria, vergas/contravergas, regularização de superfícies."))
        num += 1

        # Cobertura — se houver
        if ctx.tem_cobertura:
            secoes.append((str(num), "COBERTURA E TELHAMENTOS", "cobertura",
                            "Inclua: estrutura de cobertura, telhamento, calhas e rufos, impermeabilização."))
            num += 1

        # Instalações hidrossanitárias
        tem_hidro = any(d in ctx.disciplinas for d in
                        ['hidráulica_água_fria', 'hidráulica_esgoto', 'drenagem_pluvial'])
        if tem_hidro:
            extra = ""
            if ctx.tem_reservatorio:
                extra += " Há reservatório d'água identificado no projeto."
            if 'hidráulica_água_quente' in ctx.sistemas:
                extra += " Há instalações de água quente (chuveiros)."
            secoes.append((str(num), "INSTALAÇÕES HIDROSSANITÁRIAS", "hidráulica", extra))
            num += 1

        # Instalações elétricas
        tem_eletrica = 'instalações_elétricas' in ctx.disciplinas
        if tem_eletrica:
            extra = ""
            if ctx.tem_gerador:
                extra += " Há gerador de energia identificado."
            if ctx.tem_spda:
                extra += " Há sistema SPDA identificado."
            if 'iluminação' in ctx.sistemas:
                extra += " Há projetos de iluminação."
            if 'quadro_distribuição' in ctx.sistemas:
                extra += " Há quadros de distribuição (QDG/QD) identificados."
            secoes.append((str(num), "INSTALAÇÕES ELÉTRICAS", "elétrica", extra))
            num += 1

        # SPDA — seção própria se houver
        if ctx.tem_spda:
            secoes.append((str(num), "SISTEMA DE PROTEÇÃO CONTRA DESCARGAS ATMOSFÉRICAS (SPDA)",
                            "spda", "Detalhe subsistema de captação, descida, equalização e aterramento."))
            num += 1

        # Rede lógica / dados / CFTV
        if ctx.tem_rede_dados:
            secoes.append((str(num), "INSTALAÇÕES DE REDE LÓGICA, TELEFONIA E CFTV",
                            "rede_dados", "Inclua circuitos, equipamentos e identificação."))
            num += 1

        # Climatização
        if ctx.tem_climatizacao:
            sistemas_clim = [s for s in ctx.sistemas if 'climatiz' in s or 'condicion' in s]
            qtd_ar = sum(
                1 for t in ctx.textos_livres
                if 'ar cond' in t.lower() or 'btu' in t.lower()
            )
            secoes.append((str(num), "INSTALAÇÕES MECÂNICAS (CLIMATIZAÇÃO)",
                            "climatização",
                            f"Há aproximadamente {qtd_ar} unidades de ar-condicionado identificadas. "
                            "Inclua especificações de capacidade, instalação e manutenção."))
            num += 1

        # Combate a incêndio
        if ctx.tem_combate_incendio:
            secoes.append((str(num), "INSTALAÇÕES DE SEGURANÇA E COMBATE A INCÊNDIO",
                            "combate_incêndio",
                            "Inclua: extintores, sinalização, hidrantes (se houver)."))
            num += 1

        # Esquadrias
        if ctx.esquadrias:
            tipos = set(v.tipo for v in ctx.esquadrias.values())
            secoes.append((str(num), "ESQUADRIAS, VIDROS E FERRAGENS",
                            "esquadrias",
                            f"Tipos identificados: {', '.join(tipos)}. "
                            "Inclua portas, janelas, vidros e ferragens."))
            num += 1

        # Acabamentos — sempre
        secoes.append((str(num), "ACABAMENTOS", "acabamentos",
                        "Inclua: pisos, revestimentos, pinturas, forros, louças e metais. "
                        "Adapte ao quadro de ambientes identificados."))
        num += 1

        # Comunicações ambientais e sinalização
        secoes.append((str(num), "COMUNICAÇÕES AMBIENTAIS E SINALIZAÇÃO",
                        "sinalização",
                        "Inclua: placa obrigatória de obra, sinalização de trânsito, "
                        "sinalização de segurança e piso tátil."))
        num += 1

        # Entrega da obra — sempre
        secoes.append((str(num), "ENTREGA DA OBRA", "entrega",
                        "Inclua: ligações definitivas, ensaios/testes, limpeza final, as-built e licenças."))

        return secoes