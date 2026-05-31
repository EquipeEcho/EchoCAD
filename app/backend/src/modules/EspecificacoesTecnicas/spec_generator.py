# spec_generator.py
# Gera especificações técnicas usando a API do Groq (llama-3.3-70b-versatile).
# Recebe o contexto extraído do DXF e produz um documento Word estruturado
# seguindo o padrão do caderno de encargos do Exército Brasileiro.

import json
import logging
import os
import re
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import asyncio
import httpx

from .dxf_context_extractor import ContextoDXF
from src.exceptions import (
    NoGroqTokenException,
    OllamaUnavailableException,
    GroqQuotaExceededException,
    NoValidProviderException,
)
from src.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração da API Groq
# ---------------------------------------------------------------------------
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = settings.GROQ_MODEL
GROQ_FALLBACK_MODELS = [
    model.strip()
    for model in os.getenv("GROQ_FALLBACK_MODELS", "llama-3.1-8b-instant").split(",")
    if model.strip() and model.strip() != GROQ_MODEL
]
MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "4000"))
GROQ_TIMEOUT_SECONDS = settings.GROQ_TIMEOUT_SECONDS
GROQ_MAX_RETRIES = settings.GROQ_MAX_RETRIES
GROQ_REDUCED_MAX_TOKENS = int(os.getenv("GROQ_REDUCED_MAX_TOKENS", "2500"))


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
    subsecoes: List["SecaoEspec"] = field(default_factory=list)


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
    def __init__(self, api_key: Optional[str] = None, use_ollama: bool = False):
        """
        Inicializa SpecGenerator com suporte a Groq e Ollama.
        
        Args:
            api_key: Chave da API Groq (obrigatória se use_ollama=False)
            use_ollama: Preferência do usuário (True=Ollama, False=Groq)
        """
        self._api_key = api_key
        self._use_ollama = use_ollama
        self._ollama_model = None
        self._provider = None  # "groq" ou "ollama" - definido em auto_select_provider

    @property
    def provider(self) -> Optional[str]:
        return self._provider
        
    
    async def auto_select_provider(self) -> None:
        """
        Seleciona automaticamente o provedor de IA baseado na preferência do usuário
        e disponibilidade real dos provedores.
        
        Fluxo:
        1. Se use_ollama=True: tenta Ollama, fallback para Groq se Ollama falhar
        2. Se use_ollama=False: tenta Groq, fallback para Ollama se Groq falhar
        
        Raises:
            NoGroqTokenException: Sem token Groq e Ollama indisponível
            OllamaUnavailableException: Ollama indisponível e sem token Groq
            NoValidProviderException: Nenhum provedor está disponível
        """
        if self._use_ollama:
            # Preferência: Ollama
            logger.info("Preferência: Ollama")
            if await self._check_ollama_available():
                await self._init_ollama()
                self._provider = "ollama"
                logger.info("✓ Usando Ollama")
                return
            
            # Fallback: Groq
            logger.warning("Ollama indisponível, tentando Groq...")
            if self._api_key or settings.GROQ_API_KEY:
                self._provider = "groq"
                logger.info("✓ Usando Groq como fallback")
                return
            
            # Nenhum provedor disponível
            raise NoValidProviderException(
                "Insira um token válido do Groq ou ative o Ollama"
            )
        else:
            # Preferência: Groq
            logger.info("Preferência: Groq")
            if self._api_key or settings.GROQ_API_KEY:
                self._provider = "groq"
                logger.info("✓ Usando Groq")
                return
            
            # Fallback: Ollama
            logger.warning("Groq não disponível, tentando Ollama...")
            if await self._check_ollama_available():
                await self._init_ollama()
                self._provider = "ollama"
                logger.info("✓ Usando Ollama como fallback")
                return
            
            # Nenhum provedor disponível
            raise NoValidProviderException(
                "Insira um token válido do Groq ou ative o Ollama"
            )
    
    
    async def _check_ollama_available(self) -> bool:
        """Verifica se Ollama está respondendo"""
        from src.controller.crud_users import validate_ollama_available
        return await validate_ollama_available()

    async def _init_ollama(self) -> None:
        """Inicializa modelo Ollama via agno"""
        try:
            from agno.models.ollama import Ollama
            
            self._ollama_model = Ollama(
                id=settings.OLLAMA_MODEL,
                host=settings.OLLAMA_URL,
            )
            logger.info(
                f"Ollama inicializado: {settings.OLLAMA_URL} ({settings.OLLAMA_MODEL})"
            )
        except ImportError as e:
            logger.error(f"Erro ao importar agno.models.ollama: {e}")
            raise RuntimeError("agno package não está instalado")
        except Exception as e:
            logger.error(f"Erro ao inicializar Ollama: {e}")
            raise OllamaUnavailableException("Falha ao inicializar Ollama")



    # ------------------------------------------------------------------
    # Chamada à API com suporte a Groq e Ollama
    # ------------------------------------------------------------------
    async def _chamar_api(
        self,
        prompt_usuario: str,
        max_tokens: int = MAX_TOKENS,
        tentativas: int = GROQ_MAX_RETRIES,
        json_mode: bool = True,
    ) -> Optional[str]:
        """
        Chamada unificada para Groq (via httpx) ou Ollama (via agno).
        Garante que o provedor foi selecionado antes.
        """
        if not self._provider:
            raise RuntimeError("Provedor de IA não foi selecionado. Chame auto_select_provider() primeiro.")
        
        if self._provider == "ollama":
            return await self._chamar_ollama(prompt_usuario, max_tokens, tentativas, json_mode)
        else:
            return await self._chamar_groq(prompt_usuario, max_tokens, tentativas, json_mode)

    async def _chamar_ollama(
        self,
        prompt_usuario: str,
        max_tokens: int = MAX_TOKENS,
        tentativas: int = GROQ_MAX_RETRIES,
        json_mode: bool = True,
    ) -> Optional[str]:
        """Chamada para Ollama usando agno.models."""
        
        if not self._ollama_model:
            logger.error("Ollama model não foi inicializado")
            raise OllamaUnavailableException("Ollama não foi inicializado corretamente")
        
        for tentativa in range(tentativas):
            try:
                logger.debug(f"Ollama: tentativa {tentativa + 1}/{tentativas}")
                
                # Usar agno para gerar resposta (síncrono → thread para não bloquear event loop)
                from agno.models.message import Message as AgnoMessage
                response = await asyncio.to_thread(
                    self._ollama_model.response,
                    messages=[
                        AgnoMessage(role="system", content=SYSTEM_PROMPT),
                        AgnoMessage(role="user", content=prompt_usuario),
                    ],
                )
                
                if response and response.content:
                    return response.content
                
                if tentativa < tentativas - 1:
                    espera = min(2 ** tentativa, 10)
                    logger.warning(f"Ollama retornou vazio. Aguardando {espera}s...")
                    await asyncio.sleep(espera)
            
            except Exception as e:
                logger.error(f"Erro Ollama (tentativa {tentativa + 1}): {e}")
                if tentativa < tentativas - 1:
                    espera = min(2 ** tentativa, 10)
                    await asyncio.sleep(espera)
        
        logger.error("Ollama falhou após todas as tentativas")
        raise OllamaUnavailableException("Ollama não conseguiu processar a requisição")

    async def _chamar_groq(
        self,
        prompt_usuario: str,
        max_tokens: int = MAX_TOKENS,
        tentativas: int = GROQ_MAX_RETRIES,
        json_mode: bool = True,
    ) -> Optional[str]:
        """Chamada para Groq usando httpx (implementação original)."""
        api_key = self._api_key or settings.GROQ_API_KEY
        if not api_key:
            logger.error("GROQ_API_KEY não definida")
            raise NoGroqTokenException("Insira um token válido do Groq")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        base_payload = {
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_usuario},
            ],
        }
        if json_mode:
            base_payload["response_format"] = {"type": "json_object"}

        timeout = httpx.Timeout(
            GROQ_TIMEOUT_SECONDS,
            connect=30.0,
            read=GROQ_TIMEOUT_SECONDS,
            write=30.0,
            pool=30.0,
        )

        modelos = [GROQ_MODEL, *GROQ_FALLBACK_MODELS]
        for indice_modelo, modelo in enumerate(modelos):
            payload = {**base_payload, "model": modelo}
            if indice_modelo > 0:
                logger.warning(
                    "Tentando modelo Groq alternativo para especificacoes: %s",
                    modelo,
                )

            async with httpx.AsyncClient(timeout=timeout) as client:
                for tentativa in range(tentativas):
                    try:
                        resp = await client.post(
                            GROQ_API_URL, headers=headers, json=payload
                        )

                        # Quota excedida
                        if resp.status_code == 429:
                            error_msg = resp.json().get("error", {}).get("message", "")
                            if "quota" in error_msg.lower() or "rate_limit_exceeded" in error_msg.lower():
                                logger.error(f"Quota Groq excedida: {error_msg}")
                                raise GroqQuotaExceededException(
                                    "Limite de uso Groq atingido. Use Ollama ou renove o token"
                                )

                            import re as _re

                            if tentativa >= tentativas - 1:
                                logger.error(
                                    "Rate limit da Groq persistiu no modelo %s.",
                                    modelo,
                                )
                                break

                            msg = resp.json().get("error", {}).get("message", "")
                            m = _re.search(r"try again in ([\d.]+)s", msg)
                            espera = (
                                min(float(m.group(1)) + 2.0, 45)
                                if m
                                else min(4 * (2**tentativa), 30)
                            )
                            logger.warning(
                                f"Rate limit atingido no modelo {modelo} "
                                f"(tentativa {tentativa + 1}/{tentativas}). "
                                f"Aguardando {espera:.1f}s..."
                            )
                            await asyncio.sleep(espera)
                            continue

                        resp.raise_for_status()
                        return resp.json()["choices"][0]["message"]["content"]

                    except httpx.HTTPStatusError as e:
                        status_code = e.response.status_code
                        if status_code == 413 and payload["max_tokens"] > 2000:
                            payload["max_tokens"] = max(
                                2000, int(payload["max_tokens"] * 0.65)
                            )
                            logger.warning(
                                "Resposta solicitada grande para o modelo %s. "
                                "Repetindo com max_tokens=%s.",
                                modelo,
                                payload["max_tokens"],
                            )
                            continue
                        if status_code >= 500 and tentativa < tentativas - 1:
                            espera = min(4 * (2**tentativa), 30)
                            logger.warning(
                                f"Erro temporario Groq {status_code} no modelo {modelo} "
                                f"(tentativa {tentativa + 1}/{tentativas}). "
                                f"Aguardando {espera:.1f}s..."
                            )
                            await asyncio.sleep(espera)
                            continue
                        logger.error(
                            f"Erro HTTP Groq {status_code} no modelo {modelo}: "
                            f"{e.response.text[:500]}"
                        )
                        break
                    except httpx.RequestError as e:
                        espera = min(4 * (2**tentativa), 30)
                        if tentativa >= tentativas - 1:
                            logger.error(
                                f"Erro de request na API Groq no modelo {modelo}: {e}",
                                exc_info=True,
                            )
                            break
                        logger.warning(
                            f"Falha temporaria na API Groq no modelo {modelo} "
                            f"(tentativa {tentativa + 1}/{tentativas}, "
                            f"{type(e).__name__}): {e}. "
                            f"Aguardando {espera:.1f}s..."
                        )
                        await asyncio.sleep(espera)
                        continue
                    except Exception as e:
                        logger.error(
                            f"Erro inesperado na API Groq no modelo {modelo}: {e}",
                            exc_info=True,
                        )
                        break

        logger.error(
            "Groq nao respondeu apos tentar os modelos configurados: %s",
            ", ".join(modelos),
        )
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

    async def _chamar_com_retry(
        self, prompt: str, max_tokens: int = MAX_TOKENS, tentativas: int = 2
    ) -> Optional[dict]:
        """O backoff de rate limit ja esta em _chamar_api. Aqui so retentar se JSON vira invalido."""
        for i in range(tentativas):
            resposta = await self._chamar_api(prompt, max_tokens=max_tokens)
            if resposta is None:
                break  # erro de rede/auth — nao adianta repetir
            dados = self._extrair_json(resposta)
            if dados:
                return dados
            logger.warning(
                f"Tentativa {i + 1}/{tentativas}: JSON invalido. Repetindo..."
            )
        logger.error("Nao foi possivel obter JSON valido da API.")
        return None

    def _resumir_contexto(self, ctx: ContextoDXF) -> str:
        ambientes = [
            f"- {a.nome}: area={a.area}m2, perimetro={a.perimetro}m, "
            f"pe_direito={a.pe_direito}m, uso={a.uso or 'uso_geral'}"
            for a in ctx.ambientes[:12]
        ]
        esquadrias = [
            f"- {codigo}: {item.tipo}, quantidade={item.quantidade}"
            for codigo, item in list(ctx.esquadrias.items())[:12]
        ]

        return "\n".join(
            [
                f"Projeto: {ctx.nome_projeto}",
                f"Area total extraida: {ctx.area_total} m2",
                f"Pavimentos: {ctx.pavimentos}",
                "Disciplinas detectadas: "
                + (", ".join(sorted(ctx.disciplinas)) or "nao identificadas"),
                "Sistemas detectados: "
                + (", ".join(sorted(ctx.sistemas)) or "nao identificados"),
                "Ambientes/quantitativos principais:",
                *(ambientes or ["- Conforme quantitativos extraidos do DXF"]),
                "Esquadrias detectadas:",
                *(esquadrias or ["- Nao identificadas"]),
                "Flags tecnicas:",
                f"- SPDA: {ctx.tem_spda}",
                f"- Climatizacao: {ctx.tem_climatizacao}",
                f"- Combate a incendio: {ctx.tem_combate_incendio}",
                f"- Cobertura: {ctx.tem_cobertura}",
                f"- Drywall: {ctx.tem_drywall}",
            ]
        )

    @staticmethod
    def _contar_palavras(texto: str) -> int:
        return len(re.findall(r"\w+", texto or "", flags=re.UNICODE))

    @staticmethod
    def _lista_curta(itens: List[str], limite: int = 4) -> str:
        itens = [item for item in itens if item]
        if not itens:
            return ""
        selecionados = itens[:limite]
        if len(itens) > limite:
            selecionados.append(f"mais {len(itens) - limite} item(ns)")
        return ", ".join(selecionados)

    def _resumo_ambientes_contexto(self, ctx: ContextoDXF, limite: int = 4) -> str:
        if not ctx.ambientes:
            if ctx.area_total > 0:
                return f"area tecnica extraida de {ctx.area_total:.2f} m2"
            return "quantitativos extraidos do DXF"

        itens = []
        for ambiente in ctx.ambientes[:limite]:
            partes = [ambiente.nome]
            if ambiente.area:
                partes.append(f"{ambiente.area:.2f} m2")
            if ambiente.pe_direito:
                partes.append(f"pe-direito {ambiente.pe_direito:.2f} m")
            itens.append(" (".join([partes[0], ", ".join(partes[1:])]) + ")" if len(partes) > 1 else partes[0])
        if len(ctx.ambientes) > limite:
            itens.append(f"mais {len(ctx.ambientes) - limite} ambiente(s)")
        return "ambientes identificados: " + "; ".join(itens)

    def _resumo_extraido_contexto(self, ctx: ContextoDXF, disciplina: str = "") -> str:
        partes = [f"projeto {ctx.nome_projeto}"]
        if ctx.area_total > 0:
            partes.append(f"area total extraida de {ctx.area_total:.2f} m2")
        if ctx.pavimentos:
            partes.append(f"{ctx.pavimentos} pavimento(s)")
        partes.append(self._resumo_ambientes_contexto(ctx))

        sistemas = self._lista_curta(sorted(ctx.sistemas))
        if sistemas:
            partes.append(f"sistemas detectados: {sistemas}")

        if ctx.esquadrias:
            qtd_esquadrias = sum(item.quantidade for item in ctx.esquadrias.values())
            partes.append(f"{qtd_esquadrias} esquadria(s) identificada(s)")

        return "; ".join(partes)

    def _resumo_disciplina_contexto(self, ctx: ContextoDXF, disciplina: str) -> str:
        disciplina_normalizada = disciplina.lower()
        ambientes = self._resumo_ambientes_contexto(ctx)

        if "tecnico" in disciplina_normalizada:
            return (
                "A documentacao tecnica deve partir do levantamento extraido do DXF, "
                f"considerando {self._resumo_extraido_contexto(ctx, disciplina)}. Esses dados "
                "orientam a compatibilizacao entre memorial, quantitativos, projetos executivos, "
                "ARTs e registros de responsabilidade tecnica."
            )
        if "preliminar" in disciplina_normalizada:
            return (
                f"Os servicos preliminares devem considerar {ambientes}, alem dos acessos, "
                "frentes de trabalho e areas de apoio necessarias para executar o escopo extraido. "
                "A preparacao do local deve preservar elementos existentes, organizar o canteiro "
                "e permitir que os quantitativos sejam conferidos antes das etapas definitivas."
            )
        if "alvenaria" in disciplina_normalizada or "drywall" in disciplina_normalizada:
            return (
                f"A extracao indicou {ambientes}, servindo de base para avaliar "
                "vedacoes, panos de parede, interferencias com esquadrias e condicoes "
                "de prumo, alinhamento e acabamento."
            )
        if "estrutura" in disciplina_normalizada or "fund" in disciplina_normalizada:
            return (
                f"A disciplina estrutural deve considerar {self._resumo_extraido_contexto(ctx, disciplina)}, "
                "com verificacao de compatibilidade entre elementos extraidos, cargas previstas, "
                "apoios, cobrimentos e interferencias com arquitetura e instalacoes."
            )
        if "ele" in disciplina_normalizada or "spda" in disciplina_normalizada:
            sistemas = self._lista_curta(sorted(ctx.sistemas)) or "pontos e circuitos identificados no DXF"
            return (
                f"A extracao apontou {sistemas}, portanto a execucao deve partir da conferencia "
                "dos trajetos, alturas de instalacao, quadros, pontos de consumo e compatibilidade "
                "com os ambientes cadastrados."
            )
        if "hidr" in disciplina_normalizada or "louca" in disciplina_normalizada:
            return (
                f"Para as instalacoes hidrossanitarias, o documento deve se apoiar em {ambientes}, "
                "priorizando ambientes molhados, pontos de consumo, encaminhamentos, declividades, "
                "vedacoes e testes de estanqueidade antes da entrega."
            )
        if "esquadria" in disciplina_normalizada:
            if ctx.esquadrias:
                itens = [
                    f"{codigo} ({info.quantidade} un.)"
                    for codigo, info in list(ctx.esquadrias.items())[:4]
                ]
                detalhe = self._lista_curta(itens)
            else:
                detalhe = "esquadrias identificadas nos desenhos e quantitativos do projeto"
            return (
                f"A extracao registrou {detalhe}, exigindo conferencia de vao, sentido de abertura, "
                "nivelamento, fixacao, vedacao perimetral e acabamento junto aos revestimentos."
            )
        if "cobertura" in disciplina_normalizada:
            return (
                f"A cobertura deve ser especificada conforme {self._resumo_extraido_contexto(ctx, disciplina)}, "
                "com atencao a caimentos, arremates, calhas, rufos, estanqueidade e compatibilidade "
                "com elementos estruturais identificados."
            )

        return (
            f"A secao deve considerar {self._resumo_extraido_contexto(ctx, disciplina)}, "
            "usando os quantitativos e disciplinas detectados como referencia para definir "
            "escopo, metodo executivo, controles de qualidade e medicao."
        )

    def _texto_contextual_extracao(
        self, ctx: ContextoDXF, titulo: str, disciplina: str, campo: str = "introducao"
    ) -> str:
        contexto = self._resumo_disciplina_contexto(ctx, disciplina)
        titulo_normalizado = titulo.lower()

        if campo == "materiais":
            return (
                f"Para {titulo_normalizado}, a selecao dos materiais deve considerar o contexto "
                f"extraido do DXF: {contexto} Os produtos aplicados devem ser compativeis com "
                "as dimensoes, usos dos ambientes, interferencias indicadas e condicoes de exposicao "
                "identificadas no projeto. Antes da aplicacao, a contratada devera conferir lotes, "
                "certificados, armazenamento e integridade dos componentes, substituindo itens "
                "danificados ou incompatíveis com os quantitativos extraidos."
            )
        if campo == "execucao":
            return (
                f"A execucao de {titulo_normalizado} deve partir da conferencia dos dados extraidos: "
                f"{contexto} A equipe devera compatibilizar medidas em campo com a planta, marcar "
                "eixos, niveis e pontos de interferencia antes do inicio dos servicos. Quando houver "
                "divergencia entre desenho, quantitativo e condicao real, a fiscalizacao devera ser "
                "acionada antes da continuidade, evitando retrabalho e perda de desempenho."
            )
        if campo == "criterios":
            return (
                f"A aceitacao de {titulo_normalizado} devera verificar se o servico entregue permanece "
                f"coerente com a extracao do projeto: {contexto} A fiscalizacao deve conferir dimensoes, "
                "acabamento, alinhamento, funcionamento, registros de ensaio e compatibilidade com as "
                "demais disciplinas detectadas. Servicos fora de tolerancia, incompletos ou sem evidencia "
                "de controle devem ser corrigidos antes da medicao e do recebimento definitivo."
            )

        return (
            f"A secao de {titulo_normalizado} foi estruturada a partir do contexto extraido do DXF: "
            f"{contexto} As orientacoes tecnicas devem utilizar esses dados como base para definir "
            "escopo, prioridades de execucao, verificacoes em campo e criterios de recebimento. "
            "O objetivo e que a especificacao reflita as condicoes identificadas no projeto, sem "
            "adicionar sistemas ou ambientes que nao estejam representados na extracao."
        )

    def _normalizar_texto_contextual(
        self,
        ctx: ContextoDXF,
        valor: Any,
        titulo: str,
        disciplina: str,
        campo: str,
    ) -> str:
        texto = str(valor or "").strip()
        minimo = 35 if campo == "introducao" else 60
        if self._contar_palavras(texto) >= minimo:
            return texto

        complemento = self._texto_contextual_extracao(ctx, titulo, disciplina, campo)
        if not texto:
            return complemento
        return f"{texto} {complemento}"

    def _referencias_padrao(self, ctx: ContextoDXF) -> List[str]:
        referencias = [
            "ABNT NBR 5671 - Participacao dos intervenientes em servicos e obras de engenharia e arquitetura.",
            "ABNT NBR 13531 - Elaboracao de projetos de edificacoes - Atividades tecnicas.",
            "ABNT NBR 15575 - Edificacoes habitacionais - Desempenho.",
            "NR 18 - Condicoes e meio ambiente de trabalho na industria da construcao.",
        ]
        if "instalações_elétricas" in ctx.disciplinas:
            referencias.append(
                "ABNT NBR 5410 - Instalacoes eletricas de baixa tensao."
            )
        if any("hidráulica" in d or "hidr" in d for d in ctx.disciplinas):
            referencias.extend(
                [
                    "ABNT NBR 5626 - Sistemas prediais de agua fria e agua quente.",
                    "ABNT NBR 8160 - Sistemas prediais de esgoto sanitario.",
                ]
            )
        if "estrutura_concreto" in ctx.disciplinas:
            referencias.append(
                "ABNT NBR 6118 - Projeto de estruturas de concreto."
            )
        return referencias

    def _vida_util_padrao(self, ctx: ContextoDXF) -> List[Dict]:
        itens = [
            {
                "item": "Vedacoes e alvenarias",
                "vida_util_anos": "40 a 60",
                "garantia_anos": "5",
                "nbr": "ABNT NBR 15575",
            }
        ]
        if "estrutura_concreto" in ctx.disciplinas:
            itens.append(
                {
                    "item": "Estruturas de concreto",
                    "vida_util_anos": "50 ou superior",
                    "garantia_anos": "5",
                    "nbr": "ABNT NBR 6118",
                }
            )
        if "instalações_elétricas" in ctx.disciplinas:
            itens.append(
                {
                    "item": "Instalacoes eletricas",
                    "vida_util_anos": "20 a 30",
                    "garantia_anos": "1",
                    "nbr": "ABNT NBR 5410",
                }
            )
        return itens

    def _objeto_contextual(self, ctx: ContextoDXF, objeto_ia: Any) -> str:
        objeto = str(objeto_ia or "").strip()
        if not objeto:
            objeto = f"Execucao de obra referente ao projeto {ctx.nome_projeto}."

        detalhes = []
        if ctx.area_total > 0:
            detalhes.append(f"area tecnica extraida de {ctx.area_total:.2f} m2")
        if ctx.disciplinas:
            detalhes.append(
                "disciplinas de "
                + ", ".join(sorted(ctx.disciplinas)[:6]).replace("_", " ")
            )
        if ctx.esquadrias:
            qtd_esquadrias = sum(item.quantidade for item in ctx.esquadrias.values())
            detalhes.append(f"{qtd_esquadrias} esquadrias identificadas")

        contexto = (
            f"O escopo considerado para o projeto {ctx.nome_projeto} contempla "
            + "; ".join(detalhes)
            + "."
            if detalhes
            else f"O escopo considerado para o projeto {ctx.nome_projeto} segue os quantitativos extraidos do DXF."
        )
        complemento = (
            "A especificacao tecnica deve ser lida em conjunto com os dados extraidos "
            f"da planta, especialmente {self._resumo_ambientes_contexto(ctx)}. As disciplinas "
            "e sistemas identificados orientam os materiais, metodos executivos, verificacoes "
            "de qualidade e criterios de medicao, evitando a inclusao de servicos que nao "
            "tenham sido representados no arquivo analisado."
        )

        objeto_normalizado = objeto.lower()
        if (
            self._contar_palavras(objeto) < 70
            or ctx.nome_projeto.lower() not in objeto_normalizado
            or (ctx.area_total > 0 and "m2" not in objeto_normalizado and "m²" not in objeto_normalizado)
        ):
            return f"{objeto} {contexto} {complemento}"

        return objeto

    def _secoes_prompt(self, ctx: ContextoDXF, reduzido: bool = False) -> str:
        secoes = self._mapear_secoes(ctx)
        linhas = []
        for numero, titulo, disciplina, extra in secoes:
            linhas.append(
                f"- {numero}. {titulo} | disciplina={disciplina} | {extra or 'sem instrucoes adicionais'}"
            )
        limite = (
            "Gere 1 subsecao por secao, com textos tecnicos claros, completos e sem excesso."
            if reduzido
            else "Gere 1 subsecao por secao principal, usando 2 apenas quando o contexto justificar claramente."
        )
        return "\n".join([*linhas, limite])

    def _prompt_documento_completo(self, ctx: ContextoDXF, reduzido: bool = False) -> str:
        modo = "REDUZIDO E RESILIENTE" if reduzido else "COMPLETO E OBJETIVO"
        tamanho = (
            "Cada campo textual deve ter entre 70 e 110 palavras, com frases completas."
            if reduzido
            else "Cada campo textual deve ter entre 90 e 140 palavras, evitando respostas telegráficas."
        )
        return f"""
Gere um caderno de especificacoes tecnicas em modo {modo}.

CONTEXTO EXTRAIDO DO DXF:
{self._resumir_contexto(ctx)}

SECOES QUE DEVEM SER GERADAS:
{self._secoes_prompt(ctx, reduzido=reduzido)}

REGRAS:
- Use apenas disciplinas, sistemas e quantitativos presentes no contexto.
- Nao invente areas, ambientes, equipamentos ou sistemas nao detectados.
- Referencie normas ABNT/NR coerentes com cada disciplina.
- Em materiais, execucao e criterios, descreva requisitos de qualidade,
  tolerancias, preparo, sequencia executiva, verificacoes e medicao.
- Em cada subsecao, escreva textos em paragrafo tecnico corrido, com 3 a 5
  frases completas por campo. Explique o que deve ser usado, como executar,
  o que a fiscalizacao deve conferir e quando o servico deve ser corrigido.
- Evite frases genericas como "conforme projeto" sem detalhar o que deve ser verificado.
- O texto deve parecer um caderno de encargos profissional, nao uma lista resumida.
- Nao transforme o documento em manual extenso; priorize orientacoes praticas
  e diretamente aplicaveis ao projeto extraido do DXF.
- {tamanho}
- Responda obrigatoriamente como JSON valido.

FORMATO JSON OBRIGATORIO:
{{
  "numero_protocolo": "a ser definido",
  "objeto": "texto do objeto da obra",
  "referencias_normativas": ["norma 1", "norma 2"],
  "vida_util": [
    {{
      "item": "nome do item",
      "vida_util_anos": "valor",
      "garantia_anos": "valor",
      "nbr": "norma"
    }}
  ],
  "secoes": [
    {{
      "numero": "1",
      "titulo": "SERVICOS TECNICOS",
      "introducao": "paragrafo introdutorio da secao, com contexto tecnico e escopo",
      "subsecoes": [
        {{
          "numero": "1.1",
          "titulo": "titulo da subsecao",
          "referencias_normativas": ["ABNT NBR ..."],
          "materiais": "paragrafo tecnico sobre materiais, armazenamento e preparo",
          "execucao": "paragrafo tecnico sobre metodologia, sequencia e cuidados executivos",
          "criterios": "paragrafo tecnico sobre verificacoes, aceitacao, correcao e medicao"
        }}
      ]
    }}
  ]
}}
"""

    @staticmethod
    def _as_list(value: Any) -> List[Any]:
        return value if isinstance(value, list) else []

    def _secao_from_json(
        self,
        ctx: ContextoDXF,
        dados: Dict[str, Any],
        disciplinas_por_numero: Dict[str, str],
    ) -> Optional[SecaoEspec]:
        numero = str(dados.get("numero", "")).strip()
        titulo = str(dados.get("titulo", "")).strip()
        if not numero or not titulo:
            return None

        disciplina = disciplinas_por_numero.get(numero, "")
        subsecoes: List[SecaoEspec] = []
        for sub in self._as_list(dados.get("subsecoes")):
            if not isinstance(sub, dict):
                continue
            partes = []
            referencias = self._as_list(sub.get("referencias_normativas"))
            if referencias:
                partes.append(
                    "**Referencias Normativas:**\n"
                    + "\n".join(f"- {ref}" for ref in referencias if ref)
                )
            for chave, rotulo in (
                ("materiais", "Materiais"),
                ("execucao", "Execucao"),
                ("criterios", "Criterios de Aceitacao"),
            ):
                valor = self._normalizar_texto_contextual(
                    ctx,
                    sub.get(chave, ""),
                    str(sub.get("titulo", "")).strip() or titulo,
                    disciplina,
                    chave,
                )
                if valor:
                    partes.append(f"**{rotulo}:**\n{valor}")

            if partes:
                subsecoes.append(
                    SecaoEspec(
                        numero=str(sub.get("numero", "")).strip() or f"{numero}.1",
                        titulo=str(sub.get("titulo", "")).strip() or titulo,
                        conteudo="\n\n".join(partes),
                    )
                )

        return SecaoEspec(
            numero=numero,
            titulo=titulo,
            conteudo=self._normalizar_texto_contextual(
                ctx, dados.get("introducao", ""), titulo, disciplina, "introducao"
            ),
            subsecoes=subsecoes,
        )

    def _completar_secoes_ausentes(
        self, ctx: ContextoDXF, secoes: List[SecaoEspec]
    ) -> List[SecaoEspec]:
        existentes = {secao.numero for secao in secoes}
        for numero, titulo, disciplina, _ in self._mapear_secoes(ctx):
            if numero in existentes:
                continue
            secoes.append(
                SecaoEspec(
                    numero=numero,
                    titulo=titulo,
                    conteudo=self._texto_contextual_extracao(
                        ctx, titulo, disciplina, "introducao"
                    ),
                    subsecoes=[
                        SecaoEspec(
                            numero=f"{numero}.1",
                            titulo=f"Diretrizes extraidas para {titulo.lower()}",
                            conteudo="\n\n".join(
                                [
                                    "**Materiais:**\n"
                                    + self._texto_contextual_extracao(
                                        ctx, titulo, disciplina, "materiais"
                                    ),
                                    "**Execucao:**\n"
                                    + self._texto_contextual_extracao(
                                        ctx, titulo, disciplina, "execucao"
                                    ),
                                    "**Criterios de Aceitacao:**\n"
                                    + self._texto_contextual_extracao(
                                        ctx, titulo, disciplina, "criterios"
                                    ),
                                ]
                            ),
                        )
                    ],
                )
            )
        return sorted(secoes, key=lambda item: int(item.numero.split(".")[0]))

    def _specs_from_json(
        self, ctx: ContextoDXF, dados: Dict[str, Any]
    ) -> Optional[EspecificacoesTecnicas]:
        disciplinas_por_numero = {
            numero: disciplina
            for numero, _, disciplina, _ in self._mapear_secoes(ctx)
        }
        secoes = [
            secao
            for secao in (
                self._secao_from_json(ctx, item, disciplinas_por_numero)
                for item in self._as_list(dados.get("secoes"))
                if isinstance(item, dict)
            )
            if secao is not None
        ]
        if not secoes:
            return None

        return EspecificacoesTecnicas(
            nome_projeto=ctx.nome_projeto,
            numero_protocolo="A DEFINIR",
            objeto=self._objeto_contextual(ctx, dados.get("objeto")),
            secoes=self._completar_secoes_ausentes(ctx, secoes),
            referencias_normativas=[
                str(ref).strip()
                for ref in self._as_list(dados.get("referencias_normativas"))
                if str(ref).strip()
            ]
            or self._referencias_padrao(ctx),
            vida_util=[
                item
                for item in self._as_list(dados.get("vida_util"))
                if isinstance(item, dict)
            ]
            or self._vida_util_padrao(ctx),
        )

    async def _gerar_documento_completo(
        self, ctx: ContextoDXF, reduzido: bool = False
    ) -> Optional[EspecificacoesTecnicas]:
        prompt = self._prompt_documento_completo(ctx, reduzido=reduzido)
        dados = await self._chamar_com_retry(
            prompt,
            max_tokens=GROQ_REDUCED_MAX_TOKENS if reduzido else MAX_TOKENS,
            tentativas=1 if reduzido else 2,
        )
        if not dados:
            return None
        specs = self._specs_from_json(ctx, dados)
        if not specs:
            logger.warning("JSON da Groq nao trouxe secoes tecnicas validas.")
        return specs

    # ------------------------------------------------------------------
    # Gerar seção por disciplina
    # ------------------------------------------------------------------
    async def _gerar_secao_disciplina(
        self,
        ctx: ContextoDXF,
        numero: str,
        titulo: str,
        disciplina: str,
        instrucoes_extra: str = "",
    ) -> Optional[SecaoEspec]:

        # Selecionar ambientes relevantes para a disciplina
        if disciplina == "alvenaria":
            ambientes_rel = [
                a for a in ctx.ambientes if a.uso not in ("área_externa", "cobertura")
            ][:15]
        elif disciplina in ("hidráulica", "hidráulica_esgoto"):
            ambientes_rel = [
                a for a in ctx.ambientes if a.uso in ("sanitário", "área_alimentação")
            ][:10]
        elif disciplina == "esquadrias":
            ambientes_rel = ctx.ambientes[:10]
        else:
            ambientes_rel = ctx.ambientes[:8]

        amb_texto = (
            "\n".join(
                f"  - {a.nome}: {a.area}m², PD={a.pe_direito}m" for a in ambientes_rel
            )
            or "  - Conforme projeto"
        )

        esquadrias_texto = ""
        if ctx.esquadrias and disciplina == "esquadrias":
            esquadrias_texto = "\nEsquadrias identificadas:\n" + "\n".join(
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
- materiais: especificação técnica dos materiais, armazenamento e preparo
- execucao: metodologia, sequência executiva e cuidados de aplicação
- criterios: verificações, critérios de aceitação, correção e forma de medição

Escreva cada campo em parágrafo técnico corrido, com 4 a 6 frases completas,
sem respostas telegráficas e sem transformar o texto em manual extenso.

Retorne APENAS JSON:
{{
  "numero": "{numero}",
  "titulo": "{titulo}",
  "introducao": "texto introdutório da seção (3-5 frases)",
  "subsecoes": [
    {{
      "numero": "{numero}.1",
      "titulo": "título da subseção",
      "referencias_normativas": ["ABNT NBR XXXXX - Título", "..."],
      "materiais": "parágrafo técnico sobre materiais, armazenamento e preparo",
      "execucao": "parágrafo técnico sobre metodologia, sequência e cuidados executivos",
      "criterios": "parágrafo técnico sobre verificações, aceitação, correção e medição"
    }}
  ]
}}
"""
        dados = await self._chamar_com_retry(prompt, max_tokens=MAX_TOKENS)
        if not dados:
            logger.warning(f"Falha ao gerar seção {numero} - {titulo}")
            return None

        subsecoes = []
        for sub in dados.get("subsecoes", []):
            partes = []
            if sub.get("referencias_normativas"):
                partes.append(
                    "**Referências Normativas:**\n"
                    + "\n".join(f"- {r}" for r in sub["referencias_normativas"])
                )
            if sub.get("materiais"):
                partes.append(f"**Materiais:**\n{sub['materiais']}")
            if sub.get("execucao"):
                partes.append(f"**Execução:**\n{sub['execucao']}")
            if sub.get("criterios"):
                partes.append(f"**Critérios de Aceitação:**\n{sub['criterios']}")

            subsecoes.append(
                SecaoEspec(
                    numero=sub.get("numero", ""),
                    titulo=sub.get("titulo", ""),
                    conteudo="\n\n".join(partes),
                )
            )

        return SecaoEspec(
            numero=numero,
            titulo=titulo,
            conteudo=dados.get("introducao", ""),
            subsecoes=subsecoes,
        )

    # ------------------------------------------------------------------
    # Gerar referências normativas e vida útil
    # ------------------------------------------------------------------
    async def _gerar_referencias_e_vida_util(self, ctx: ContextoDXF) -> Dict:
        prompt = f"""
Para um projeto de construção civil com as seguintes disciplinas e sistemas:
- Disciplinas: {", ".join(sorted(ctx.disciplinas))}
- Sistemas: {", ".join(sorted(ctx.sistemas))}

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
        dados = await self._chamar_com_retry(prompt, max_tokens=2000)
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
    async def gerar(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        """Chamado pelo __init__.py — gera todas as seções."""
        return await self._orquestrar(ctx)

    async def gerar_especificacao(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        """Alias para compatibilidade com versões anteriores do test_especificacoes.py."""
        return await self._orquestrar(ctx)

    async def _orquestrar(self, ctx: ContextoDXF) -> EspecificacoesTecnicas:
        logger.info(f"Iniciando geração de specs para: {ctx.nome_projeto}")

        specs = await self._gerar_documento_completo(ctx)
        if specs:
            logger.info(
                f"  Especificacoes geradas em chamada unica: {len(specs.secoes)} secoes"
            )
            return specs

        logger.warning(
            "Chamada principal da Groq falhou. Tentando modo reduzido em chamada unica."
        )
        specs = await self._gerar_documento_completo(ctx, reduzido=True)
        if specs:
            logger.info(
                f"  Especificacoes geradas em modo reduzido: {len(specs.secoes)} secoes"
            )
            return specs

        raise RuntimeError(
            "Nao foi possivel gerar as especificacoes tecnicas pela IA da Groq. "
            "Verifique a chave, o limite da conta ou tente novamente em alguns minutos."
        )

    # ------------------------------------------------------------------
    # Mapeamento de seções baseado no contexto da planta
    # ------------------------------------------------------------------
    def _mapear_secoes(self, ctx: ContextoDXF) -> List[tuple]:
        secoes = []
        num = 1

        secoes.append(
            (
                str(num),
                "SERVIÇOS TÉCNICOS",
                "tecnico",
                "Inclua: Elaboração de Projetos Executivos, ART, mão de obra especializada.",
            )
        )
        num += 1

        secoes.append(
            (
                str(num),
                "SERVIÇOS PRELIMINARES",
                "preliminar",
                "Inclua: limpeza inicial, topografia, sondagem, canteiro de obras, demolições.",
            )
        )
        num += 1

        if any("fundações" in d or "escavação" in d.lower() for d in ctx.disciplinas):
            secoes.append(
                (
                    str(num),
                    "MOVIMENTO DE SOLO",
                    "movimento_solo",
                    "Inclua: escavações, aterros, nivelamentos e compactações.",
                )
            )
            num += 1

        tem_estrutura = any(
            d in ctx.disciplinas
            for d in ["estrutura_concreto", "fundações", "estrutura_cobertura"]
        )
        if tem_estrutura or ctx.tem_estrutura_metalica:
            extra = ""
            if ctx.tem_estrutura_metalica:
                extra += (
                    " O projeto possui estruturas metálicas identificadas nas plantas."
                )
            if "estrutura_cobertura" in ctx.disciplinas:
                extra += " Há estrutura de cobertura a ser executada."
            secoes.append((str(num), "SISTEMAS ESTRUTURAIS", "estrutura", extra))
            num += 1

        secoes.append(
            (
                str(num),
                "ALVENARIAS",
                "alvenaria",
                f"O projeto tem drywall: {ctx.tem_drywall}. "
                "Inclua alvenaria, drywall, vergas/contravergas.",
            )
        )
        num += 1

        if ctx.tem_cobertura:
            secoes.append(
                (
                    str(num),
                    "COBERTURA E TELHAMENTOS",
                    "cobertura",
                    "Inclua: estrutura de cobertura, telhamento, calhas, rufos, impermeabilização.",
                )
            )
            num += 1

        tem_hidro = any(
            d in ctx.disciplinas
            for d in ["hidráulica_água_fria", "hidráulica_esgoto", "drenagem_pluvial"]
        )
        if tem_hidro:
            extra = ""
            if ctx.tem_reservatorio:
                extra += " Há reservatório d'água identificado."
            if "hidráulica_água_quente" in ctx.sistemas:
                extra += " Há instalações de água quente (chuveiros)."
            secoes.append(
                (str(num), "INSTALAÇÕES HIDROSSANITÁRIAS", "hidráulica", extra)
            )
            num += 1

        if "instalações_elétricas" in ctx.disciplinas:
            extra = ""
            if ctx.tem_gerador:
                extra += " Há gerador de energia identificado."
            if ctx.tem_spda:
                extra += " Há sistema SPDA identificado."
            if "iluminação" in ctx.sistemas:
                extra += " Há projeto de iluminação."
            if "quadro_distribuição" in ctx.sistemas:
                extra += " Há QDG/QD identificados."
            secoes.append((str(num), "INSTALAÇÕES ELÉTRICAS", "elétrica", extra))
            num += 1

        if ctx.tem_spda:
            secoes.append(
                (
                    str(num),
                    "SPDA - SISTEMA DE PROTEÇÃO CONTRA DESCARGAS ATMOSFÉRICAS",
                    "spda",
                    "Detalhe captação, descida, equalização e aterramento.",
                )
            )
            num += 1

        if ctx.tem_rede_dados:
            secoes.append(
                (
                    str(num),
                    "INSTALAÇÕES DE REDE LÓGICA, TELEFONIA E CFTV",
                    "rede_dados",
                    "Inclua circuitos, equipamentos e identificação.",
                )
            )
            num += 1

        if ctx.tem_climatizacao:
            qtd_ar = sum(
                1
                for t in ctx.textos_livres
                if "ar cond" in t.lower() or "btu" in t.lower()
            )
            secoes.append(
                (
                    str(num),
                    "INSTALAÇÕES MECÂNICAS (CLIMATIZAÇÃO)",
                    "climatização",
                    f"Aproximadamente {qtd_ar} unidades identificadas. "
                    "Inclua capacidade, instalação e manutenção.",
                )
            )
            num += 1

        if ctx.tem_combate_incendio:
            secoes.append(
                (
                    str(num),
                    "INSTALAÇÕES DE SEGURANÇA E COMBATE A INCÊNDIO",
                    "combate_incêndio",
                    "Inclua: extintores, sinalização, hidrantes.",
                )
            )
            num += 1

        if ctx.esquadrias:
            tipos = set(v.tipo for v in ctx.esquadrias.values())
            secoes.append(
                (
                    str(num),
                    "ESQUADRIAS, VIDROS E FERRAGENS",
                    "esquadrias",
                    f"Tipos identificados: {', '.join(tipos)}. "
                    "Inclua portas, janelas, vidros e ferragens.",
                )
            )
            num += 1

        secoes.append(
            (
                str(num),
                "ACABAMENTOS",
                "acabamentos",
                "Inclua: pisos, revestimentos, pinturas, forros, louças e metais.",
            )
        )
        num += 1

        secoes.append(
            (
                str(num),
                "COMUNICAÇÕES AMBIENTAIS E SINALIZAÇÃO",
                "sinalização",
                "Inclua: placa de obra, sinalização de trânsito, segurança e piso tátil.",
            )
        )
        num += 1

        secoes.append(
            (
                str(num),
                "ENTREGA DA OBRA",
                "entrega",
                "Inclua: ligações definitivas, testes, limpeza final, as-built e licenças.",
            )
        )

        return secoes
