# dxf_context_extractor.py
# Extrai contexto rico do arquivo DXF para alimentar a geração de
# especificações técnicas via IA. Coleta: ambientes, disciplinas presentes,
# sistemas identificados, esquadrias, estrutura e revestimentos.

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mapeamento de layers → disciplinas / sistemas
# ---------------------------------------------------------------------------
LAYER_DISCIPLINAS = {
    # Arquitetura
    "arq - alvenaria alta": "alvenaria",
    "arq - alvenaria média-baixa": "alvenaria",
    "arq - alvenaria (-)": "alvenaria",
    "arquitetônico - alvenaria alta": "alvenaria",
    "arq - esquadrias": "esquadrias",
    "esquadrias": "esquadrias",
    "arq - dry-wall": "drywall",
    "arq - cobertura": "cobertura",
    "arq - mobiliário": "mobiliário",
    "arq - escadas": "escadas",
    "arq - grades": "grades",
    "arq - cercamentos": "cercamentos",
    "arq - desnível": "desníveis",
    "arq - guias calçadas sarjetas": "pavimentação",
    # Estrutural
    "estrutural - pilares": "estrutura_concreto",
    "estrutural - vigas": "estrutura_concreto",
    "estrutural - lajes": "estrutura_concreto",
    "estrutural - fundações": "fundações",
    "est-vigas cobertura existente": "estrutura_cobertura",
    # Hidrossanitário
    "hidrossanitário - água fria": "hidráulica_água_fria",
    "hidrossanitário - esgoto": "hidráulica_esgoto",
    "hidrossanitário - ventilação": "hidráulica_ventilação",
    "hidrossanitário - água pluvial": "drenagem_pluvial",
    "hidrossanitário - mobiliário": "louças_metais",
    # Elétrica
    "elétrica": "instalações_elétricas",
    "ele-circuito": "instalações_elétricas",
    "ele-fiação": "instalações_elétricas",
    "ele-fiação1": "instalações_elétricas",
    "ele-textos": "instalações_elétricas",
    "ele-malha spda": "spda",
    "ele-malha terra": "spda",
    "ele-haste cobreada": "spda",
    "ele-cordoalha": "spda",
    "ele-terminal aéreo": "spda",
    "ele-tubo descida": "spda",
    "ele-cx. inspeção": "spda",
    # Lógica / Dados
    "lógica - dados telefonia cftv": "rede_lógica_cftv",
    # Contra incêndio
    "contra incêndio": "combate_incêndio",
}

# Palavras-chave em textos que revelam sistemas
KEYWORDS_SISTEMAS = {
    "ar cond": "climatização",
    "ar-cond": "climatização",
    "18000btu": "climatização",
    "12000btu": "climatização",
    "9000btu": "climatização",
    "chuveiro": "hidráulica_água_quente",
    "vaso sanitário": "louças_metais",
    "torneira": "louças_metais",
    "lavatório": "louças_metais",
    "gerador": "gerador_energia",
    "reservatório": "reservação_água",
    "spda": "spda",
    "extintor": "combate_incêndio",
    "luminária": "iluminação",
    "emergência": "iluminação_emergência",
    "qd": "quadro_distribuição",
    "qdg": "quadro_distribuição",
    "interruptor": "instalações_elétricas",
    "tomada": "instalações_elétricas",
    "radier": "estrutura_concreto",
    "mureta": "alvenaria",
    "container": "canteiro_obras",
    "drywall": "drywall",
    "divisória": "drywall",
    "calçada": "pavimentação",
    "asfalto": "pavimentação",
    "telhado": "cobertura",
    "telha": "cobertura",
    "muro": "cercamentos",
    "piso cerâmico": "revestimentos",
    "porcelanato": "revestimentos",
    "pintura": "pintura",
}


# ---------------------------------------------------------------------------
# Dataclasses de Contexto
# ---------------------------------------------------------------------------
@dataclass
class AmbienteDXF:
    nome: str
    area: float
    perimetro: float
    pe_direito: float
    subtitulo: str = ""
    uso: str = ""  # inferido: sanitário, escritório, etc.


@dataclass
class EsquadriaDXF:
    tag: str
    tipo: str  # Porta, Janela
    largura: float
    altura: float
    quantidade: int = 1


@dataclass
class ContextoDXF:
    nome_projeto: str
    area_total: float = 0.0
    ambientes: List[AmbienteDXF] = field(default_factory=list)
    disciplinas: Set[str] = field(default_factory=set)
    sistemas: Set[str] = field(default_factory=set)
    esquadrias: Dict[str, EsquadriaDXF] = field(default_factory=dict)
    textos_livres: List[str] = field(default_factory=list)

    # Flags de presença de sistemas críticos
    tem_spda: bool = False
    tem_gerador: bool = False
    tem_reservatorio: bool = False
    tem_climatizacao: bool = False
    tem_combate_incendio: bool = False
    tem_drywall: bool = False
    tem_cobertura: bool = False
    tem_rede_dados: bool = False
    tem_estrutura_metalica: bool = False


# ---------------------------------------------------------------------------
# Extrator DXF
# ---------------------------------------------------------------------------
class DXFContextExtractor:
    def __init__(self, filepath: str, nome_projeto: str = "Projeto"):
        self.filepath = Path(filepath)
        self.nome_projeto = nome_projeto
        self._ctx = ContextoDXF(nome_projeto=nome_projeto)

    def extrair(self) -> ContextoDXF:
        """Extração manual de baixo nível (sem ezdxf para máxima portabilidade)."""
        if not self.filepath.exists():
            return self._ctx

        try:
            with open(
                self.filepath, "r", encoding="windows-1252", errors="replace"
            ) as f:
                lines = f.readlines()
        except Exception as e:
            logger.error(f"Erro ao ler DXF: {e}")
            return self._ctx

        current_type = None
        current_layer = None
        current_text = None
        current_handle = None

        # Buffer para MTEXT
        mtext_buffer = []
        is_mtext = False

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == "0":
                # Finaliza entidade anterior
                if is_mtext and mtext_buffer:
                    full_text = "".join(mtext_buffer)
                    self._processar_entidade("MTEXT", current_layer, full_text)
                    is_mtext = False
                    mtext_buffer = []

                current_type = lines[i + 1].strip()
                current_layer = None
                current_text = None
                is_mtext = current_type == "MTEXT"
                i += 2
                continue

            code = line
            val = lines[i + 1].strip()

            if code == "8":
                current_layer = val.lower()
            elif code == "1":
                if is_mtext:
                    mtext_buffer.append(val)
                else:
                    current_text = val
                    self._processar_entidade(current_type, current_layer, current_text)
            elif code == "3":  # Parte de MTEXT longo
                if is_mtext:
                    mtext_buffer.append(val)

            i += 2

        self._consolidar_contexto()
        return self._ctx

    def _processar_entidade(self, etype: str, layer: str, text: str):
        if not layer:
            return

        # 1. Mapear Disciplinas por Layer
        for prefix, disc in LAYER_DISCIPLINAS.items():
            if layer.startswith(prefix):
                self._ctx.disciplinas.add(disc)

        # 2. Detectar Sistemas por Texto
        if text:
            clean_text = self._limpar_texto(text)
            if clean_text:
                self._ctx.textos_livres.append(clean_text)
                for key, sistema in KEYWORDS_SISTEMAS.items():
                    if key in clean_text.lower():
                        self._ctx.sistemas.add(sistema)

        # 3. Identificar Presença de Macros
        l_low = layer.lower()
        if "spda" in l_low or "descida" in l_low:
            self._ctx.tem_spda = True
        if "gerador" in l_low:
            self._ctx.tem_gerador = True
        if "reservatório" in l_low or "caixa d" in l_low:
            self._ctx.tem_reservatorio = True
        if "cobertura" in l_low or "telhado" in l_low:
            self._ctx.tem_cobertura = True
        if "metálica" in l_low or "perfis" in l_low:
            self._ctx.tem_estrutura_metalica = True
        if "dry-wall" in l_low or "drywall" in l_low:
            self._ctx.tem_drywall = True

    def _limpar_texto(self, raw: str) -> str:
        # Remove formatações de MTEXT do CAD (\P, \fArial|b0...)
        t = re.sub(r"\\[Pp]", " ", raw)
        t = re.sub(r"\\f[^;]*;", "", t)
        t = re.sub(r"\\[AHWQC][^;]*;", "", t)
        t = re.sub(r"[{}]", "", t)
        return t.strip()

    def _consolidar_contexto(self):
        """Tenta inferir ambientes e área total a partir dos textos livres."""
        # 1. Agrupar textos que parecem ser de ambientes
        # Padrão: Nome \n Área m² \n P=... \n PD=...

        # Como o parser é linear e simples, vamos procurar sequências
        # ou textos que contenham "m²"

        possiveis_ambientes = []

        for i, txt in enumerate(self._ctx.textos_livres):
            if "m²" in txt.lower():
                # Tenta pegar o nome (geralmente o texto anterior ou a linha anterior)
                area = self._extrair_valor(txt, r"([\d,.]+)\s*m²")
                if area is None:
                    continue

                nome = "Ambiente"
                perimetro = 0.0
                pd = 3.0

                # Se o texto for multiline (limpo), tenta quebrar
                parts = txt.split()
                if len(parts) > 0 and not parts[0][0].isdigit():
                    nome = parts[0]

                # Tenta buscar P e PD no mesmo texto ou nos vizinhos
                p_val = self._extrair_valor(txt, r"P\s*=\s*([\d,.]+)")
                pd_val = self._extrair_valor(txt, r"PD\s*=\s*([\d,.]+)")

                if p_val:
                    perimetro = p_val
                if pd_val:
                    pd = pd_val

                self._ctx.ambientes.append(
                    AmbienteDXF(
                        nome=nome.upper(), area=area, perimetro=perimetro, pe_direito=pd
                    )
                )
                self._ctx.area_total += area

        # 2. Dedução de flags por sistemas
        if "climatização" in self._ctx.sistemas:
            self._ctx.tem_climatizacao = True
        if "combate_incêndio" in self._ctx.sistemas:
            self._ctx.tem_combate_incendio = True
        if "rede_lógica_cftv" in self._ctx.disciplinas:
            self._ctx.tem_rede_dados = True

        # Limpeza
        self._ctx.disciplinas.discard(None)
        self._ctx.sistemas.discard(None)

    def _extrair_valor(self, texto: str, regex: str) -> Optional[float]:
        m = re.search(regex, texto, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).replace(",", "."))
            except:
                return None
        return None
