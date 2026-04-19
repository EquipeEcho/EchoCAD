
# dxf_extractor.py
# Extrai dados de ambientes diretamente das anotações de texto do arquivo DXF.
# A planta já contém área, perímetro e pé-direito nos próprios textos —
# esse módulo lê esses valores em vez de recalcular geometria.

import logging
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Layers que contêm os textos de nome/área/perímetro/pé-direito dos ambientes
# ---------------------------------------------------------------------------
LAYERS_TEXTO = {
    'arq - textos',
    'arquitetônico - textos',
}

LAYERS_PAREDE = {
    'arq - alvenaria alta',
    'arq - alvenaria média-baixa',
    'arq - alvenaria (-)',
    'arquitetônico - alvenaria alta',
}
LAYERS_VAO = {
    'arq - esquadrias',
    'esquadrias',
}

ESPESSURA_PADRAO = 0.15  # m
ALTURA_PADRAO    = 3.00  # m


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
@dataclass
class Ambiente:
    nome: str
    subtitulo: Optional[str] = None
    area: float = 0.0
    perimetro: float = 0.0
    pe_direito: float = 3.0
    espessura_parede: float = ESPESSURA_PADRAO

    comprimento_paredes: float = 0.0
    comprimento_vaos: float = 0.0

    area_bruta_parede: float = 0.0
    area_vaos: float = 0.0
    area_liquida_parede: float = 0.0

    custo_unitario: float = 0.0
    custo_total: float = 0.0

    cx: float = 0.0
    cy: float = 0.0


@dataclass
class ProjetoMemorial:
    nome_projeto: str
    ambientes: List[Ambiente]


# ---------------------------------------------------------------------------
# Parser DXF manual (sem ezdxf)
# ---------------------------------------------------------------------------
class DXFParser:
    ENCODING = 'windows-1252'

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._lines: List[str] = []
        self._entities: List[Dict] = []

    def load(self) -> bool:
        try:
            with open(self.filepath, 'r', encoding=self.ENCODING, errors='replace') as f:
                self._lines = [l.rstrip('\r\n') for l in f.readlines()]
            logger.info(f"DXF carregado: {len(self._lines)} linhas")
            return True
        except Exception as e:
            logger.error(f"Erro ao abrir DXF: {e}")
            return False

    def _find_section_bounds(self, section_name: str) -> Tuple[Optional[int], Optional[int]]:
        start = None
        for i, l in enumerate(self._lines):
            if l.strip() == section_name and i > 0 and self._lines[i - 1].strip() == '2':
                start = i
                break
        if start is None:
            return None, None
        end = None
        for i in range(start, len(self._lines)):
            if self._lines[i].strip() == 'ENDSEC' and i > 0 and self._lines[i - 1].strip() == '0':
                end = i
                break
        return start, end

    def parse_entities(self) -> List[Dict]:
        if self._entities:
            return self._entities

        start, end = self._find_section_bounds('ENTITIES')
        if start is None:
            logger.error("Seção ENTITIES não encontrada.")
            return []

        entities = []
        current_type: Optional[str] = None
        current_data: Dict = defaultdict(list)

        i = start + 1
        while i < end - 1:
            try:
                code = int(self._lines[i].strip())
                value = self._lines[i + 1].strip()
                if code == 0:
                    if current_type:
                        entities.append({'type': current_type, 'data': dict(current_data)})
                    current_type = value
                    current_data = defaultdict(list)
                else:
                    current_data[code].append(value)
                i += 2
            except ValueError:
                i += 1

        if current_type:
            entities.append({'type': current_type, 'data': dict(current_data)})

        self._entities = entities
        logger.info(f"Entidades parseadas: {len(entities)}")
        return entities


# ---------------------------------------------------------------------------
# Extrator de ambientes
# ---------------------------------------------------------------------------
class CADExtractor:
    ALTURA_VAO_PADRAO = 2.10  # m

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._parser = DXFParser(filepath)
        self._loaded = self._parser.load()

    @staticmethod
    def _limpar_mtext(raw: str) -> str:
        # Remover formatação de parágrafo inicial (\pxqc; etc.)
        t = re.sub(r'\\p[^;]*;', '', raw, flags=re.IGNORECASE)
        # Remover outras formatações (\f, \H, \W, \C, \L etc.)
        t = re.sub(r'\\[fFhHwWqQaAcClLtToOC][^;]*;', '', t)
        t = re.sub(r'\\[~{}\|]', '', t)
        # \P = quebra de parágrafo → newline
        t = t.replace('\\P', '\n').replace('\\p', '\n')
        # Remover chaves de grupo {  }
        t = t.replace('{', '').replace('}', '')
        return t.strip()

    @staticmethod
    def _parse_float_br(s: str) -> Optional[float]:
        m = re.search(r'([\d]+[,.][\d]+)', s)
        if m:
            return float(m.group(1).replace(',', '.'))
        m2 = re.search(r'(\d+)', s)
        return float(m2.group(1)) if m2 else None

    def _parse_area(self, s: str) -> Optional[float]:
        if re.match(r'^[\d,\.]+\s*m²$', s.strip()):
            return self._parse_float_br(s)
        return None

    def _parse_perimetro(self, s: str) -> Optional[float]:
        if re.match(r'^P\s*=', s.strip(), re.I):
            return self._parse_float_br(s)
        return None

    def _parse_pe_direito(self, s: str) -> Optional[float]:
        if re.match(r'^PD\s*=', s.strip(), re.I):
            return self._parse_float_br(s)
        return None

    @staticmethod
    def _comprimento_line(data: Dict) -> float:
        try:
            x1, y1 = float(data[10][0]), float(data[20][0])
            x2 = float(data[11][0]) if 11 in data else (float(data[10][1]) if len(data.get(10,[])) > 1 else x1)
            y2 = float(data[21][0]) if 21 in data else (float(data[20][1]) if len(data.get(20,[])) > 1 else y1)
            return math.hypot(x2 - x1, y2 - y1)
        except Exception:
            return 0.0

    @staticmethod
    def _comprimento_lwpolyline(data: Dict) -> float:
        try:
            xs = [float(v) for v in data.get(10, [])]
            ys = [float(v) for v in data.get(20, [])]
            if len(xs) < 2:
                return 0.0
            return sum(math.hypot(xs[i+1]-xs[i], ys[i+1]-ys[i]) for i in range(len(xs)-1))
        except Exception:
            return 0.0

    def extrair_dados_reais(self) -> List[Ambiente]:
        if not self._loaded:
            return []

        entities = self._parser.parse_entities()

        # ---- 1. Agrupar textos por posição (x, y) ----
        grupos: Dict[Tuple[float, float], List[str]] = defaultdict(list)

        for e in entities:
            layer = e['data'].get(8, [''])[0].lower().strip()
            if layer not in LAYERS_TEXTO:
                continue
            if e['type'] not in ('TEXT', 'MTEXT'):
                continue

            raw = e['data'].get(1, [''])[0]
            texto = self._limpar_mtext(raw)
            if not texto:
                continue

            x = round(float(e['data'].get(10, ['0'])[0]), 1)
            y = round(float(e['data'].get(20, ['0'])[0]), 1)
            grupos[(x, y)].append(texto)

        # ---- 2. Interpretar cada grupo como um ambiente ----
        NOMES_IGNORADOS = {
            'legenda', 'p = perímetro', 'pd = pé direito', 'baixa', 'média',
            'alta', 'interruptor', 'existente', 'a demolir', 'a construir',
            'nao sofre', 'não sofre', 'intervenção', 'arquitetônico',
        }
        PREFIXOS_IGNORADOS = (
            'pm', 'pa', 'pd', 'pv', 'pf', 'ja', 'jr', 'jf', 'rg', 'rp',
            '%%', 'vb', '{legenda', 'p =', 'pd =', 'telhado',
            'bloco', 'pátio', 'circu-', 'lação', 'container', 'gerador',
            'isométrico', '{', 'pm*', 'ja*', 'centro',
        )

        ambientes_dict: Dict[str, Ambiente] = {}

        for (x, y), textos in grupos.items():
            nome = None
            subtitulo = None
            area = None
            perimetro = None
            pe_direito = None

            for bloco in textos:
                for linha in bloco.split('\n'):
                    linha = linha.strip()
                    if not linha:
                        continue

                    v_area = self._parse_area(linha)
                    v_per  = self._parse_perimetro(linha)
                    v_pd   = self._parse_pe_direito(linha)

                    if v_area is not None and area is None:
                        area = v_area
                    elif v_per is not None and perimetro is None:
                        perimetro = v_per
                    elif v_pd is not None and pe_direito is None:
                        pe_direito = v_pd
                    elif re.match(r'^\(', linha):
                        subtitulo = linha.strip('()')
                    elif (
                        nome is None
                        and len(linha) >= 3
                        and linha.lower() not in NOMES_IGNORADOS
                        and not any(linha.lower().startswith(p) for p in PREFIXOS_IGNORADOS)
                        and re.match(r'^[A-ZÁÉÍÓÚÀÂÊÎÔÛÃÕ]', linha)
                        and not re.match(r'^[\d]', linha)
                    ):
                        nome = linha

            if not nome or area is None:
                continue

            # Normalizar "CIRCU-" / "LAÇÃO" que aparecem em dois MTEXTs
            if nome.upper() in ('CIRCU-', 'LAÇÃO'):
                nome = 'CIRCULAÇÃO'

            chave = f"{nome}|{area}"
            if chave in ambientes_dict:
                continue

            ambientes_dict[chave] = Ambiente(
                nome=nome,
                subtitulo=subtitulo,
                area=area,
                perimetro=perimetro or 0.0,
                pe_direito=pe_direito or ALTURA_PADRAO,
                cx=x,
                cy=y,
            )

        if not ambientes_dict:
            logger.warning("Nenhum ambiente encontrado pelo parser de texto.")
            return []

        ambientes_lista = list(ambientes_dict.values())
        logger.info(f"Ambientes identificados: {len(ambientes_lista)}")

        # ---- 3. Comprimentos geométricos (enriquecimento) ----
        for e in entities:
            layer = e['data'].get(8, [''])[0].lower().strip()
            etype = e['type']

            is_parede = layer in LAYERS_PAREDE
            is_vao    = layer in LAYERS_VAO

            if not (is_parede or is_vao):
                continue

            if etype == 'LINE':
                comp = self._comprimento_line(e['data'])
                try:
                    cx = (float(e['data'][10][0]) + float(e['data'].get(11, [e['data'][10][0]])[0])) / 2
                    cy = (float(e['data'][20][0]) + float(e['data'].get(21, [e['data'][20][0]])[0])) / 2
                except Exception:
                    continue
            elif etype == 'LWPOLYLINE':
                comp = self._comprimento_lwpolyline(e['data'])
                xs = [float(v) for v in e['data'].get(10, ['0'])]
                ys = [float(v) for v in e['data'].get(20, ['0'])]
                cx = sum(xs) / len(xs) if xs else 0
                cy = sum(ys) / len(ys) if ys else 0
            else:
                continue

            if comp <= 0:
                continue

            # Normalizar unidade
            if comp > 1000:
                comp /= 1000
            elif comp > 100:
                comp /= 100

            melhor = min(ambientes_lista, key=lambda a: math.hypot(a.cx - cx, a.cy - cy), default=None)
            if melhor is None:
                continue

            if is_parede:
                melhor.comprimento_paredes += comp
            else:
                melhor.comprimento_vaos += comp

        # ---- 4. Calcular áreas de parede ----
        for amb in ambientes_lista:
            p  = amb.perimetro if amb.perimetro > 0 else amb.comprimento_paredes
            pd = amb.pe_direito
            ev = self.ALTURA_VAO_PADRAO

            amb.comprimento_paredes  = round(amb.comprimento_paredes, 2)
            amb.comprimento_vaos     = round(amb.comprimento_vaos, 2)
            amb.area_bruta_parede    = round(p * pd, 2)
            amb.area_vaos            = round(amb.comprimento_vaos * ev, 2)
            amb.area_liquida_parede  = round(max(amb.area_bruta_parede - amb.area_vaos, 0), 2)

        # ---- 5. Limpeza: remover entradas com dados implausíveis ----
        resultado = []
        for amb in ambientes_lista:
            # Sem perímetro e com área de parede absurda: remover
            if amb.perimetro <= 0 and amb.area_bruta_parede > amb.area * 50:
                logger.warning(
                    f"Removendo '{amb.nome}' ({amb.area}m²): "
                    f"área bruta de parede implausível ({amb.area_bruta_parede:.1f}m²)")
                continue
            # Garantir que área líquida não excede área bruta
            if amb.area_liquida_parede > amb.area_bruta_parede:
                amb.area_liquida_parede = amb.area_bruta_parede
                amb.area_vaos = 0.0
            resultado.append(amb)

        resultado.sort(key=lambda a: (a.nome, -a.area))
        return resultado