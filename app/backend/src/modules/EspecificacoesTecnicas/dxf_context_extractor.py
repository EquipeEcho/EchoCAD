# dxf_context_extractor.py
# Extrai contexto rico do arquivo DXF para alimentar a geração de
# especificações técnicas via IA. Coleta: ambientes, disciplinas presentes,
# sistemas identificados, esquadrias, estrutura e revestimentos.

import logging
import math
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
    'arq - alvenaria alta':         'alvenaria',
    'arq - alvenaria média-baixa':  'alvenaria',
    'arq - alvenaria (-)':          'alvenaria',
    'arquitetônico - alvenaria alta': 'alvenaria',
    'arq - esquadrias':             'esquadrias',
    'esquadrias':                   'esquadrias',
    'arq - dry-wall':               'drywall',
    'arq - cobertura':              'cobertura',
    'arq - mobiliário':             'mobiliário',
    'arq - escadas':                'escadas',
    'arq - grades':                 'grades',
    'arq - cercamentos':            'cercamentos',
    'arq - desnível':               'desníveis',
    'arq - guias calçadas sarjetas': 'pavimentação',
    # Estrutural
    'estrutural - pilares':         'estrutura_concreto',
    'estrutural - vigas':           'estrutura_concreto',
    'estrutural - lajes':           'estrutura_concreto',
    'estrutural - fundações':       'fundações',
    'est-vigas cobertura existente': 'estrutura_cobertura',
    # Hidrossanitário
    'hidrossanitário - água fria':   'hidráulica_água_fria',
    'hidrossanitário - esgoto':      'hidráulica_esgoto',
    'hidrossanitário - ventilação':  'hidráulica_ventilação',
    'hidrossanitário - água pluvial': 'drenagem_pluvial',
    'hidrossanitário - mobiliário':  'louças_metais',
    # Elétrica
    'elétrica':                     'instalações_elétricas',
    'ele-circuito':                 'instalações_elétricas',
    'ele-fiação':                   'instalações_elétricas',
    'ele-fiação1':                  'instalações_elétricas',
    'ele-textos':                   'instalações_elétricas',
    'ele-malha spda':               'spda',
    'ele-malha terra':              'spda',
    'ele-haste cobreada':           'spda',
    'ele-cordoalha':                'spda',
    'ele-terminal aéreo':           'spda',
    'ele-tubo descida':             'spda',
    'ele-cx. inspeção':             'spda',
    # Lógica / Dados
    'lógica - dados telefonia cftv': 'rede_lógica_cftv',
    # Contra incêndio
    'contra incêndio':              'combate_incêndio',
}

# Palavras-chave em textos que revelam sistemas
KEYWORDS_SISTEMAS = {
    'ar cond':          'climatização',
    'ar-cond':          'climatização',
    '18000btu':         'climatização',
    '12000btu':         'climatização',
    '9000btu':          'climatização',
    'chuveiro':         'hidráulica_água_quente',
    'vaso sanitário':   'louças_metais',
    'torneira':         'louças_metais',
    'lavatório':        'louças_metais',
    'gerador':          'gerador_energia',
    'reservatório':     'reservação_água',
    'spda':             'spda',
    'extintor':         'combate_incêndio',
    'luminária':        'iluminação',
    'emergência':       'iluminação_emergência',
    'qd':               'quadro_distribuição',
    'qdg':              'quadro_distribuição',
    'interruptor':      'instalações_elétricas',
    'tomada':           'instalações_elétricas',
    'radier':           'estrutura_concreto',
    'mureta':           'alvenaria',
    'container':        'canteiro_obras',
    'drywall':          'drywall',
    'divisória':        'drywall',
    'calçada':          'pavimentação',
    'asfalto':          'pavimentação',
    'telhado':          'cobertura',
    'telha':            'cobertura',
    'muro':             'cercamentos',
    'piso cerâmico':    'revestimentos',
    'porcelanato':      'revestimentos',
    'pintura':          'pintura',
}

# Esquadrias: prefixos usados nos textos da planta
PREFIXOS_ESQUADRIAS = {
    'ja': 'Janela de Alumínio',
    'jf': 'Janela de Ferro',
    'jr': 'Janela com Régua',
    'pm': 'Porta de Madeira',
    'pa': 'Porta de Alumínio',
    'pv': 'Porta de Vidro',
    'pf': 'Porta de Ferro',
    'pd': 'Porta Double',
}


# ---------------------------------------------------------------------------
# Dataclasses de contexto
# ---------------------------------------------------------------------------
@dataclass
class AmbienteInfo:
    nome: str
    subtitulo: Optional[str]
    area: float
    perimetro: float
    pe_direito: float
    uso: str = ''               # inferido pelo nome


@dataclass
class EsquadriaInfo:
    codigo: str
    tipo: str
    quantidade: int = 1


@dataclass
class ContextoDXF:
    """Contexto completo extraído do DXF para geração de specs técnicas."""
    nome_projeto: str
    ambientes: List[AmbienteInfo] = field(default_factory=list)
    disciplinas: Set[str] = field(default_factory=set)
    sistemas: Set[str] = field(default_factory=set)
    esquadrias: Dict[str, EsquadriaInfo] = field(default_factory=dict)
    tem_spda: bool = False
    tem_climatizacao: bool = False
    tem_gerador: bool = False
    tem_reservatorio: bool = False
    tem_combate_incendio: bool = False
    tem_rede_dados: bool = False
    tem_cobertura: bool = False
    tem_estrutura_metalica: bool = False
    tem_drywall: bool = False
    area_total: float = 0.0
    pavimentos: int = 1
    layers_encontrados: List[str] = field(default_factory=list)
    textos_livres: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'nome_projeto': self.nome_projeto,
            'area_total': round(self.area_total, 2),
            'pavimentos': self.pavimentos,
            'ambientes': [
                {
                    'nome': a.nome,
                    'subtitulo': a.subtitulo,
                    'area': a.area,
                    'perimetro': a.perimetro,
                    'pe_direito': a.pe_direito,
                    'uso': a.uso,
                }
                for a in self.ambientes
            ],
            'disciplinas': sorted(self.disciplinas),
            'sistemas': sorted(self.sistemas),
            'esquadrias': {
                k: {'tipo': v.tipo, 'quantidade': v.quantidade}
                for k, v in self.esquadrias.items()
            },
            'flags': {
                'tem_spda': self.tem_spda,
                'tem_climatizacao': self.tem_climatizacao,
                'tem_gerador': self.tem_gerador,
                'tem_reservatorio': self.tem_reservatorio,
                'tem_combate_incendio': self.tem_combate_incendio,
                'tem_rede_dados': self.tem_rede_dados,
                'tem_cobertura': self.tem_cobertura,
                'tem_estrutura_metalica': self.tem_estrutura_metalica,
                'tem_drywall': self.tem_drywall,
            },
        }


# ---------------------------------------------------------------------------
# Parser DXF (sem dependências externas)
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
            return True
        except Exception as e:
            logger.error(f"Erro ao abrir DXF: {e}")
            return False

    def _find_section(self, name: str):
        start = None
        for i, l in enumerate(self._lines):
            if l.strip() == name and i > 0 and self._lines[i - 1].strip() == '2':
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

        start, end = self._find_section('ENTITIES')
        if start is None:
            return []

        entities = []
        current_type = None
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
        return entities


# ---------------------------------------------------------------------------
# Extrator de contexto
# ---------------------------------------------------------------------------
class DXFContextExtractor:

    LAYERS_TEXTO = {'arq - textos', 'arquitetônico - textos'}

    def __init__(self, filepath: str, nome_projeto: str = ''):
        self.filepath = filepath
        self.nome_projeto = nome_projeto or Path(filepath).stem.title()
        self._parser = DXFParser(filepath)
        self._loaded = self._parser.load()

    @staticmethod
    def _limpar_mtext(raw: str) -> str:
        t = re.sub(r'\\p[^;]*;', '', raw, flags=re.IGNORECASE)
        t = re.sub(r'\\[fFhHwWqQaAcClLtToOC][^;]*;', '', t)
        t = re.sub(r'\\[~{}\|]', '', t)
        t = t.replace('\\P', '\n').replace('\\p', '\n')
        t = t.replace('{', '').replace('}', '')
        return t.strip()

    @staticmethod
    def _parse_float(s: str) -> Optional[float]:
        m = re.search(r'([\d]+[,.][\d]+)', s)
        if m:
            return float(m.group(1).replace(',', '.'))
        m2 = re.search(r'(\d+)', s)
        return float(m2.group(1)) if m2 else None

    @staticmethod
    def _inferir_uso(nome: str) -> str:
        n = nome.lower()
        if any(k in n for k in ['banheiro', 'wc', 'sanitário']):
            return 'sanitário'
        if any(k in n for k in ['alojamento', 'dormitório', 'quarto']):
            return 'dormitório'
        if any(k in n for k in ['sala', 'auditório', 'reunião']):
            return 'área_administrativa'
        if any(k in n for k in ['copa', 'cozinha', 'refeitório']):
            return 'área_alimentação'
        if any(k in n for k in ['circulação', 'passadiço', 'corredor', 'hall']):
            return 'circulação'
        if any(k in n for k in ['depósito', 'almoxarifado', 'reserva']):
            return 'depósito'
        if any(k in n for k in ['calçada', 'pátio', 'área externa', 'área']):
            return 'área_externa'
        if 'telhado' in n:
            return 'cobertura'
        return 'uso_geral'

    def extrair(self) -> ContextoDXF:
        if not self._loaded:
            return ContextoDXF(nome_projeto=self.nome_projeto)

        entities = self._parser.parse_entities()
        ctx = ContextoDXF(nome_projeto=self.nome_projeto)

        # ---- 1. Layers presentes ----
        layers_raw: Set[str] = set()
        for e in entities:
            layer = e['data'].get(8, [''])[0].strip()
            if layer:
                layers_raw.add(layer)
        ctx.layers_encontrados = sorted(layers_raw)

        # ---- 2. Mapear disciplinas pelos layers ----
        for layer in layers_raw:
            layer_l = layer.lower()
            for key, disciplina in LAYER_DISCIPLINAS.items():
                if key in layer_l:
                    ctx.disciplinas.add(disciplina)
                    break

        # ---- 3. Extrair ambientes dos textos ----
        grupos: Dict = defaultdict(list)
        textos_livres_raw: List[str] = []

        for e in entities:
            layer = e['data'].get(8, [''])[0].lower().strip()
            if layer not in self.LAYERS_TEXTO:
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
            textos_livres_raw.append(texto.lower())

        # Parsear ambientes
        SKIP_NOMES = {
            'legenda', 'p = perímetro', 'pd = pé direito', 'baixa', 'média',
            'alta', 'interruptor', 'existente', 'a demolir', 'a construir',
            'não sofre', 'intervenção', 'arquitetônico',
        }
        SKIP_PREFIXOS = (
            'pm', 'pa', 'pd', 'pv', 'pf', 'ja', 'jr', 'jf', 'rg', 'rp',
            '%%', 'vb', '{legenda', 'p =', 'pd =', 'telhado', 'bloco',
            'pátio', 'circu-', 'lação', 'container', 'gerador', '{', 'centro',
        )

        ambientes_vistos: Set[str] = set()

        for (x, y), textos in grupos.items():
            nome = subtitulo = area = perimetro = pe_direito = None

            for bloco in textos:
                for linha in bloco.split('\n'):
                    linha = linha.strip()
                    if not linha:
                        continue
                    if re.match(r'^[\d,\.]+\s*m²$', linha):
                        if area is None:
                            area = self._parse_float(linha)
                    elif re.match(r'^P\s*=', linha, re.I):
                        if perimetro is None:
                            perimetro = self._parse_float(linha)
                    elif re.match(r'^PD\s*=', linha, re.I):
                        if pe_direito is None:
                            pe_direito = self._parse_float(linha)
                    elif re.match(r'^\(', linha):
                        subtitulo = linha.strip('()')
                    elif (
                        nome is None
                        and len(linha) >= 3
                        and linha.lower() not in SKIP_NOMES
                        and not any(linha.lower().startswith(p) for p in SKIP_PREFIXOS)
                        and re.match(r'^[A-ZÁÉÍÓÚÀÂÊÎÔÛÃÕ]', linha)
                        and not re.match(r'^\d', linha)
                    ):
                        nome = linha

            if not nome or area is None:
                continue
            if nome.upper() in ('CIRCU-', 'LAÇÃO'):
                nome = 'CIRCULAÇÃO'

            chave = f"{nome}|{area}"
            if chave in ambientes_vistos:
                continue
            ambientes_vistos.add(chave)

            # Filtrar áreas com perímetro implausível
            if area is not None and perimetro is None and area > 500:
                continue

            ctx.ambientes.append(AmbienteInfo(
                nome=nome,
                subtitulo=subtitulo,
                area=area or 0,
                perimetro=perimetro or 0,
                pe_direito=pe_direito or 3.0,
                uso=self._inferir_uso(nome),
            ))
            ctx.area_total += area or 0

        ctx.area_total = round(ctx.area_total, 2)

        # ---- 4. Detectar esquadrias nos textos ----
        esquadrias_count: Dict[str, int] = defaultdict(int)
        for texto in textos_livres_raw:
            for linha in texto.split('\n'):
                linha = linha.strip()
                for prefixo, tipo in PREFIXOS_ESQUADRIAS.items():
                    if re.match(rf'^{prefixo}\d', linha, re.I):
                        codigo = linha[:3].upper()
                        esquadrias_count[codigo] += 1

        for codigo, qtd in esquadrias_count.items():
            prefixo = codigo[:2].lower()
            tipo = PREFIXOS_ESQUADRIAS.get(prefixo, 'Esquadria')
            ctx.esquadrias[codigo] = EsquadriaInfo(
                codigo=codigo, tipo=tipo, quantidade=qtd
            )

        # ---- 5. Detectar sistemas via keywords nos textos ----
        todos_textos = ' '.join(textos_livres_raw).lower()

        for keyword, sistema in KEYWORDS_SISTEMAS.items():
            if keyword in todos_textos:
                ctx.sistemas.add(sistema)

        # ---- 6. Detectar via layers textos específicos ----
        for e in entities:
            layer = e['data'].get(8, [''])[0].lower().strip()
            raw = e['data'].get(1, [''])[0].lower()

            if 'spda' in layer or 'malha' in layer or 'aterramento' in layer:
                ctx.sistemas.add('spda')
            if 'incêndio' in layer:
                ctx.sistemas.add('combate_incêndio')
            if 'lógica' in layer or 'dados' in layer or 'cftv' in layer:
                ctx.sistemas.add('rede_lógica_cftv')
            if 'dry-wall' in layer:
                ctx.sistemas.add('drywall')

        # ---- 7. Flags de sistemas ----
        ctx.tem_spda             = 'spda' in ctx.sistemas or 'spda' in ctx.disciplinas
        ctx.tem_climatizacao     = 'climatização' in ctx.sistemas
        ctx.tem_gerador          = 'gerador_energia' in ctx.sistemas
        ctx.tem_reservatorio     = 'reservação_água' in ctx.sistemas
        ctx.tem_combate_incendio = 'combate_incêndio' in ctx.sistemas
        ctx.tem_rede_dados       = 'rede_lógica_cftv' in ctx.sistemas or 'rede_lógica_cftv' in ctx.disciplinas
        ctx.tem_cobertura        = 'cobertura' in ctx.disciplinas or 'cobertura' in ctx.sistemas
        ctx.tem_drywall          = 'drywall' in ctx.sistemas or 'drywall' in ctx.disciplinas
        ctx.tem_estrutura_metalica = any(
            'metalica' in l or 'metal' in l or 'est-vigas' in l
            for l in [ll.lower() for ll in ctx.layers_encontrados]
        )

        # ---- 8. Adicionar textos livres relevantes (para contexto IA) ----
        relevantes = set()
        for e in entities:
            layer = e['data'].get(8, [''])[0].lower().strip()
            if layer not in self.LAYERS_TEXTO:
                continue
            raw = e['data'].get(1, [''])[0]
            texto = self._limpar_mtext(raw).strip()
            if texto and len(texto) > 5 and not re.match(r'^[\d,\.]+', texto):
                for linha in texto.split('\n'):
                    linha = linha.strip()
                    if len(linha) > 8 and linha not in relevantes:
                        relevantes.add(linha)

        ctx.textos_livres = sorted(relevantes)[:60]  # limitar tokens

        logger.info(
            f"Contexto DXF: {len(ctx.ambientes)} ambientes | "
            f"{len(ctx.disciplinas)} disciplinas | "
            f"{len(ctx.sistemas)} sistemas | "
            f"área total: {ctx.area_total}m²"
        )
        return ctx
