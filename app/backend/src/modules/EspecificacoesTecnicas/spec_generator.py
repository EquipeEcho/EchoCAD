# spec_generator.py
# Gera especificações técnicas usando a configuração centralizada de IA (Groq ou Ollama).
# Recebe o contexto extraído do DXF e produz um documento Word estruturado
# seguindo o padrão do caderno de encargos do Exército Brasileiro.

import json
import logging
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from agno.agent import Agent
from src.aiconf import high_model

from .dxf_context_extractor import ContextoDXF

logger = logging.getLogger(__name__)


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
- Para cada seção, inclua: Referências Normativas, Materiais, Execução e
  Critérios de Aceitação/Medição.
- Adapte o conteúdo ao contexto real extraído da planta.
- Não invente sistemas que não foram identificados na planta.
- Responda APENAS com JSON válido, sem markdown, sem explicações.
""").strip()


# ---------------------------------------------------------------------------
# Dataclasses de resultado
# ---------------------------------------------------------------------------
@dataclass
class SecaoEspec:
    numero: str
    titulo: str
    conteudo: str
    subsecoes: List['SecaoEspec'] = field(default_factory=list)


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

    def __init__(self):
        """Inicializa o gerador com a configuração centralizada de IA."""
        logger.info(f"Inicializando SpecGenerator com modelo: {high_model}")
        self.agent = Agent(
            name="spec-generator",
            model=high_model,
            instructions=[SYSTEM_PROMPT],
        )

    # ------------------------------------------------------------------
    # Chamada à API de IA (Groq ou Ollama via aiconf)
    # ------------------------------------------------------------------
    def _chamar_api(self, prompt_usuario: str) -> Optional[str]:
        """Chama a IA configurada (Groq ou Ollama) via agno."""
        try:
            logger.debug(f"Chamando IA para gerar especificações...")
            resposta = self.agent.run(prompt_usuario, stream=False)
            
            if resposta:
                # Extrai o conteúdo da resposta
                if hasattr(resposta, 'content'):
                    return resposta.content
                elif isinstance(resposta, str):
                    return resposta
                else:
                    return str(resposta)
            else:
                logger.error("IA retornou resposta vazia")
                return None

        except Exception as e:
            logger.error(f"Erro ao chamar IA: {e}")
            return None

    # ------------------------------------------------------------------
    # Extrair JSON da resposta (tolerante a markdown e texto extra)
    # ------------------------------------------------------------------
    @staticmethod
    def _extrair_json(texto: str) -> Optional[dict]:
        if not texto:
            return None
        import re as _re
        limpo = _re.sub(r"```(?:json)?", "", texto).replace("```", "").strip()
        try:
            return json.loads(limpo)
        except Exception:
            pass
        m = _re.search(r"\{.*\}", limpo, _re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        logger.warning("Nao foi possivel extrair JSON da resposta.")
        return None

    def _chamar_com_retry(self, prompt: str, tentativas: int = 3) -> Optional[dict]:
        """Chama a IA com retry se JSON vier inválido."""
        for i in range(tentativas):
            resposta = self._chamar_api(prompt)
            if resposta is None:
                break  # erro de rede/auth — nao adianta repetir
            dados = self._extrair_json(resposta)
            if dados:
                return dados
            logger.warning(f"Tentativa {i+1}/{tentativas}: JSON invalido. Repetindo...")
        logger.error("Nao foi possivel obter JSON valido da IA.")
        return None


    # ------------------------------------------------------------------
    # Gerar objeto e contexto geral
    # ------------------------------------------------------------------
    def _gerar_objeto_e_contexto(self, ctx: ContextoDXF) -> Dict:
        ambientes_resumo = [
            f"{a.nome}{' (' + a.subtitulo + ')' if a.subtitulo else ''}: "
            f"{a.area}m² | P={a.perimetro}m | PD={a.pe_direito}m"
            for a in ctx.ambientes[:30]
        ]

        prompt = f"""
Com base no contexto extraído da planta CAD do projeto, gere os textos de
abertura do caderno de especificações técnicas.

CONTEXTO DO PROJETO:
- Nome: {ctx.nome_projeto}
- Área total: {ctx.area_total}m²
- Disciplinas identificadas: {', '.join(sorted(ctx.disciplinas))}
- Sistemas identificados: {', '.join(sorted(ctx.sistemas))}
- Ambientes principais:
{chr(10).join('  - ' + a for a in ambientes_resumo)}

Retorne APENAS um JSON com esta estrutura:
{{
  "numero_protocolo": "a ser definido",
  "objeto": "texto descrevendo o objeto da obra (2-4 frases)",
  "finalidade": "texto descrevendo a finalidade (2-3 frases)",
  "concepcao": "texto descrevendo a concepção do projeto (3-5 frases)"
}}
"""
        dados = self._chamar_com_retry(prompt)
        if not dados:
            return {
                "numero_protocolo": "A DEFINIR",
                "objeto": f"Execução de obras de construção e reforma nas instalações do projeto {ctx.nome_projeto}.",
                "finalidade": "As presentes especificações técnicas têm por finalidade descrever os serviços a serem executados pela contratada.",
                "concepcao": f"O projeto compreende a construção e adequação de ambientes com área total de {ctx.area_total}m².",
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
        instrucoes_extra: str = '',
    ) -> Optional[SecaoEspec]:

        # Selecionar ambientes relevantes para a disciplina
        if disciplina == 'alvenaria':
            ambientes_rel = [a for a in ctx.ambientes if a.uso not in ('área_externa', 'cobertura')][:15]
        elif disciplina in ('hidráulica', 'hidráulica_esgoto'):
            ambientes_rel = [a for a in ctx.ambientes if a.uso in ('sanitário', 'área_alimentação')][:10]
        elif disciplina == 'esquadrias':
            ambientes_rel = ctx.ambientes[:10]
        else:
            ambientes_rel = ctx.ambientes[:8]

        amb_texto = '\n'.join(f"  - {a.nome}: {a.area}m², PD={a.pe_direito}m" for a in ambientes_rel) \
                    or "  - Conforme projeto"

        esquadrias_texto = ''
        if ctx.esquadrias and disciplina == 'esquadrias':
            esquadrias_texto = '\nEsquadrias identificadas:\n' + '\n'.join(
                f"  - {k}: {v.tipo} ({v.quantidade} un.)"
                for k, v in list(ctx.esquadrias.items())[:10]
            )

        prompt = f"""
Gere a seção "{numero}. {titulo}" do caderno de especificações técnicas.

CONTEXTO:
- Projeto: {ctx.nome_projeto}
- Área total: {ctx.area_total}m²
- Ambientes para este serviço:
{amb_texto}{esquadrias_texto}
{instrucoes_extra}

Para cada subseção inclua obrigatoriamente:
- referencias_normativas: lista de NBRs pertinentes
- materiais: especificação técnica dos materiais
- execucao: passo a passo do processo construtivo
- criterios: critérios de aceitação e forma de medição

Retorne APENAS JSON:
{{
  "numero": "{numero}",
  "titulo": "{titulo}",
  "introducao": "texto introdutório da seção (2-4 frases)",
  "subsecoes": [
    {{
      "numero": "{numero}.1",
      "titulo": "título da subseção",
      "referencias_normativas": ["ABNT NBR XXXXX - Título", "..."],
      "materiais": "especificação detalhada dos materiais",
      "execucao": "descrição detalhada do processo executivo",
      "criterios": "critérios de aceitação e forma de medição"
    }}
  ]
}}
"""
        dados = self._chamar_com_retry(prompt)
        if not dados:
            logger.warning(f"Falha ao gerar seção {numero} - {titulo}")
            return None

        subsecoes = []
        for sub in dados.get('subsecoes', []):
            partes = []
            if sub.get('referencias_normativas'):
                partes.append("**Referências Normativas:**\n" +
                              '\n'.join(f"- {r}" for r in sub['referencias_normativas']))
            if sub.get('materiais'):
                partes.append(f"**Materiais:**\n{sub['materiais']}")
            if sub.get('execucao'):
                partes.append(f"**Execução:**\n{sub['execucao']}")
            if sub.get('criterios'):
                partes.append(f"**Critérios de Aceitação:**\n{sub['criterios']}")

            subsecoes.append(SecaoEspec(
                numero=sub.get('numero', ''),
                titulo=sub.get('titulo', ''),
                conteudo='\n\n'.join(partes),
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
        prompt = f"""
Para um projeto de construção civil com as seguintes disciplinas e sistemas:
- Disciplinas: {', '.join(sorted(ctx.disciplinas))}
- Sistemas: {', '.join(sorted(ctx.sistemas))}

Gere a lista de referências normativas ABNT e a tabela de vida útil.

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
      "nbr": "XXXXX"
    }}
  ]
}}
"""
        dados = self._chamar_com_retry(prompt)
        if not dados:
            return {
                "referencias_normativas": [
                    "ABNT NBR 5671 - Participação dos intervenientes em serviços e obras de engenharia e arquitetura.",
                    "ABNT NBR 7678 - Segurança na execução de obras e serviços de construção.",
                    "ABNT NBR 13531 - Elaboração de projetos de edificações - Atividades técnicas.",
                ],
                "vida_util": [],
            }
        return dados

    # ------------------------------------------------------------------
    # Orquestrador principal
    # ------------------------------------------------------------------
    def gerar(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        """Chamado pelo __init__.py — gera todas as seções."""
        return self._orquestrar(ctx)

    def gerar_especificacao(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        """Alias para compatibilidade com versões anteriores do test_especificacoes.py."""
        return self._orquestrar(ctx)

    def _orquestrar(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        logger.info(f"Iniciando geração de specs para: {ctx.nome_projeto}")

        abertura  = self._gerar_objeto_e_contexto(ctx)
        refs_vida = self._gerar_referencias_e_vida_util(ctx)
        secoes_map = self._mapear_secoes(ctx)

        secoes: List[SecaoEspec] = []
        for num, titulo, disciplina, extra in secoes_map:
            logger.info(f"  Gerando seção {num}: {titulo}...")
            secao = self._gerar_secao_disciplina(ctx, num, titulo, disciplina, extra)
            if secao:
                secoes.append(secao)

        return EspecificacoesTecnicas(
            nome_projeto=ctx.nome_projeto,
            numero_protocolo=abertura.get('numero_protocolo', 'A DEFINIR'),
            objeto=abertura.get('objeto', ''),
            secoes=secoes,
            referencias_normativas=refs_vida.get('referencias_normativas', []),
            vida_util=refs_vida.get('vida_util', []),
        )

    # ------------------------------------------------------------------
    # Mapeamento de seções baseado no contexto da planta
    # ------------------------------------------------------------------
    def _mapear_secoes(self, ctx: ContextoDXF) -> List[tuple]:
        secoes = []
        num = 1

        secoes.append((str(num), "SERVIÇOS TÉCNICOS", "tecnico",
                       "Inclua: Elaboração de Projetos Executivos, ART, mão de obra especializada."))
        num += 1

        secoes.append((str(num), "SERVIÇOS PRELIMINARES", "preliminar",
                       "Inclua: limpeza inicial, topografia, sondagem, canteiro de obras, demolições."))
        num += 1

        if any('fundações' in d or 'escavação' in d.lower() for d in ctx.disciplinas):
            secoes.append((str(num), "MOVIMENTO DE SOLO", "movimento_solo",
                           "Inclua: escavações, aterros, nivelamentos e compactações."))
            num += 1

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

        secoes.append((str(num), "ALVENARIAS", "alvenaria",
                       f"O projeto tem drywall: {ctx.tem_drywall}. "
                       "Inclua alvenaria, drywall, vergas/contravergas."))
        num += 1

        if ctx.tem_cobertura:
            secoes.append((str(num), "COBERTURA E TELHAMENTOS", "cobertura",
                           "Inclua: estrutura de cobertura, telhamento, calhas, rufos, impermeabilização."))
            num += 1

        tem_hidro = any(d in ctx.disciplinas for d in
                        ['hidráulica_água_fria', 'hidráulica_esgoto', 'drenagem_pluvial'])
        if tem_hidro:
            extra = ""
            if ctx.tem_reservatorio:
                extra += " Há reservatório d'água identificado."
            if 'hidráulica_água_quente' in ctx.sistemas:
                extra += " Há instalações de água quente (chuveiros)."
            secoes.append((str(num), "INSTALAÇÕES HIDROSSANITÁRIAS", "hidráulica", extra))
            num += 1

        if 'instalações_elétricas' in ctx.disciplinas:
            extra = ""
            if ctx.tem_gerador:   extra += " Há gerador de energia identificado."
            if ctx.tem_spda:      extra += " Há sistema SPDA identificado."
            if 'iluminação' in ctx.sistemas: extra += " Há projeto de iluminação."
            if 'quadro_distribuição' in ctx.sistemas: extra += " Há QDG/QD identificados."
            secoes.append((str(num), "INSTALAÇÕES ELÉTRICAS", "elétrica", extra))
            num += 1

        if ctx.tem_spda:
            secoes.append((str(num), "SPDA - SISTEMA DE PROTEÇÃO CONTRA DESCARGAS ATMOSFÉRICAS",
                           "spda", "Detalhe captação, descida, equalização e aterramento."))
            num += 1

        if ctx.tem_rede_dados:
            secoes.append((str(num), "INSTALAÇÕES DE REDE LÓGICA, TELEFONIA E CFTV",
                           "rede_dados", "Inclua circuitos, equipamentos e identificação."))
            num += 1

        if ctx.tem_climatizacao:
            qtd_ar = sum(1 for t in ctx.textos_livres if 'ar cond' in t.lower() or 'btu' in t.lower())
            secoes.append((str(num), "INSTALAÇÕES MECÂNICAS (CLIMATIZAÇÃO)", "climatização",
                           f"Aproximadamente {qtd_ar} unidades identificadas. "
                           "Inclua capacidade, instalação e manutenção."))
            num += 1

        if ctx.tem_combate_incendio:
            secoes.append((str(num), "INSTALAÇÕES DE SEGURANÇA E COMBATE A INCÊNDIO",
                           "combate_incêndio", "Inclua: extintores, sinalização, hidrantes."))
            num += 1

        if ctx.esquadrias:
            tipos = set(v.tipo for v in ctx.esquadrias.values())
            secoes.append((str(num), "ESQUADRIAS, VIDROS E FERRAGENS", "esquadrias",
                           f"Tipos identificados: {', '.join(tipos)}. "
                           "Inclua portas, janelas, vidros e ferragens."))
            num += 1

        secoes.append((str(num), "ACABAMENTOS", "acabamentos",
                       "Inclua: pisos, revestimentos, pinturas, forros, louças e metais."))
        num += 1

        secoes.append((str(num), "COMUNICAÇÕES AMBIENTAIS E SINALIZAÇÃO", "sinalização",
                       "Inclua: placa de obra, sinalização de trânsito, segurança e piso tátil."))
        num += 1

        secoes.append((str(num), "ENTREGA DA OBRA", "entrega",
                       "Inclua: ligações definitivas, testes, limpeza final, as-built e licenças."))

        return secoes