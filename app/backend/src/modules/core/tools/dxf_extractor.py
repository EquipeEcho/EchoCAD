import math
import re
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from ezdxf.filemanagement import readfile
from ezdxf.document import Drawing
from ezdxf.lldxf.const import DXFError

logger = logging.getLogger(__name__)


LAYERS_TEXTO = {'arq - textos', 'arquitetônico - textos'}
LAYERS_PAREDE = {'arq - alvenaria alta', 'arq - alvenaria média-baixa', 'arq - alvenaria (-)', 'arquitetônico - alvenaria alta'}
LAYERS_VAO = {'arq - esquadrias', 'esquadrias'}

ESPESSURA_PADRAO = 0.15
ALTURA_PADRAO = 3.00

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

# ---------------------------------------------------------------------------
# Extrator de ambientes com EZDXF
# ---------------------------------------------------------------------------
class CADExtractorEZDXF:
    ALTURA_VAO_PADRAO = 2.10

    def __init__(self, doc: Drawing):
        try:
            # O ezdxf lida automaticamente com a versão do DXF e o encoding
            self.doc = doc
            self.msp = self.doc.modelspace()
            self._loaded = True
            logger.info("DXF carregado com sucesso via ezdxf.")
        except DXFError:
            logger.error(f"Erro: Arquivo DXF inválido ou corrompido.")
            self._loaded = False

    @staticmethod
    def _parse_float_br(s: str) -> Optional[float]:
        m = re.search(r'([\d]+[,.][\d]+)', s)
        if m: return float(m.group(1).replace(',', '.'))
        m2 = re.search(r'(\d+)', s)
        return float(m2.group(1)) if m2 else None

    def identificar_ambientes(self) -> List[Ambiente]:
        """
        PARTE 1: Apenas identifica onde estão os ambientes e seus nomes/áreas.
        Este é o 'Cérebro' que serve para todas as outras disciplinas.
        """
        grupos = defaultdict(list)
        for entity in self.msp:
            if entity.dxf.layer.lower().strip() not in LAYERS_TEXTO: continue
            if entity.dxftype() not in ('TEXT', 'MTEXT'): continue
            
            texto = entity.plain_text() if entity.dxftype() == 'MTEXT' else entity.dxf.text
            x, y = round(entity.dxf.insert.x, 1), round(entity.dxf.insert.y, 1)
            grupos[(x, y)].append(texto.strip())

        ambientes_dict = {}
        for (x, y), textos in grupos.items():
            nome, area, perimetro, pe_direito = None, None, None, None
            for bloco in textos:
                for linha in bloco.split('\n'):
                    linha = linha.strip()
                    if re.match(r'^[\d,\.]+\s*m²$', linha): area = self._parse_float_br(linha)
                    elif re.match(r'^P\s*=', linha, re.I): perimetro = self._parse_float_br(linha)
                    elif re.match(r'^PD\s*=', linha, re.I): pe_direito = self._parse_float_br(linha)
                    elif (nome is None and len(linha) >= 3 and not re.match(r'^[\d\(]', linha)):
                        nome = linha

            if nome and area is not None:
                chave = f"{nome}|{area}"
                ambientes_dict[chave] = Ambiente(
                    nome=nome, area=area, perimetro=perimetro or 0.0,
                    pe_direito=pe_direito or ALTURA_PADRAO, cx=x, cy=y
                )
        return list(ambientes_dict.values())
    
    def extrair_eletrica(self, ambientes_lista: List[Ambiente]):
        """
        PARTE 3: Pega os mesmos ambientes e conta itens elétricos.
        """
        LAYERS_PONTOS = {'ele - tomadas', 'ele - interruptores'}
        LAYERS_FIOS = {'ele - fiação', 'ele - eletrodutos'}
        
        # Estrutura para guardar os resultados
        for amb in ambientes_lista:
            amb.contagem_dispositivos = defaultdict(int) # Adicionando dinamicamente
            amb.metros_fio = 0.0

        for entity in self.msp:
            layer = entity.dxf.layer.lower().strip()
            
            # 1. Contar Caixas/Interruptores (Blocos)
            if entity.dxftype() == 'INSERT' and layer in LAYERS_PONTOS:
                cx, cy = entity.dxf.insert.x, entity.dxf.insert.y
                nome_item = entity.dxf.name
                
                melhor = min(ambientes_lista, key=lambda a: math.hypot(a.cx - cx, a.cy - cy))
                melhor.contagem_dispositivos[nome_item] += 1

            # 2. Medir Comprimento de Fios (Linhas/Polilinhas)
            elif entity.dxftype() in ('LINE', 'LWPOLYLINE') and layer in LAYERS_FIOS:
                comp = 0.0
                if entity.dxftype() == 'LINE':
                    comp = math.dist(entity.dxf.start[:2], entity.dxf.end[:2])
                    mx, my = (entity.dxf.start.x + entity.dxf.end.x)/2, (entity.dxf.start.y + entity.dxf.end.y)/2
                else:
                    v = list(entity.vertices())
                    comp = sum(math.dist(v[i][:2], v[i+1][:2]) for i in range(len(v)-1))
                    mx, my = v[0][0], v[0][1]

                melhor = min(ambientes_lista, key=lambda a: math.hypot(a.cx - mx, a.cy - my))
                melhor.metros_fio += comp

    def calcular_alvenaria(self, ambientes_lista: List[Ambiente]):
        """
        PARTE 2: Processa geometria de paredes e vãos e vincula aos ambientes.
        """
        if not ambientes_lista:
            logger.warning("Nenhum ambiente fornecido para calcular alvenaria.")
            return

        for entity in self.msp:
            layer = entity.dxf.layer.lower().strip()
            is_parede = layer in LAYERS_PAREDE
            is_vao = layer in LAYERS_VAO

            # Só processa se a layer for de interesse
            if not (is_parede or is_vao):
                continue

            comp = 0.0
            cx, cy = 0.0, 0.0
            dxftype = entity.dxftype()

            # --- Extração de Comprimento e Centroide ---
            if dxftype == 'LINE':
                comp = math.dist((entity.dxf.start.x, entity.dxf.start.y), 
                                 (entity.dxf.end.x, entity.dxf.end.y))
                cx = (entity.dxf.start.x + entity.dxf.end.x) / 2
                cy = (entity.dxf.start.y + entity.dxf.end.y) / 2

            elif dxftype == 'LWPOLYLINE':
                pontos = list(entity.vertices())
                if len(pontos) > 1:
                    # Soma distâncias entre todos os vértices da polilinha
                    comp = sum(math.dist(pontos[i][:2], pontos[i+1][:2]) for i in range(len(pontos)-1))
                    # Centroide simplificado (média dos vértices)
                    cx = sum(p[0] for p in pontos) / len(pontos)
                    cy = sum(p[1] for p in pontos) / len(pontos)

            if comp <= 0: 
                continue

            # Normalização de unidade (se estiver em mm ou cm, converte para metros)
            if comp > 1000: comp /= 1000
            elif comp > 100: comp /= 100

            # --- Vinculação por Proximidade ---
            # Busca o ambiente cujo texto (extraído na Parte 1) está mais perto desta linha
            melhor = min(ambientes_lista, key=lambda a: math.hypot(a.cx - cx, a.cy - cy), default=None)
            
            if melhor:
                if is_parede:
                    melhor.comprimento_paredes += comp
                else:
                    melhor.comprimento_vaos += comp

        # --- Finalização dos Cálculos de Área ---
        for amb in ambientes_lista:
            # Se não houver perímetro digitado no texto, usa a soma das paredes detectadas
            p = amb.perimetro if amb.perimetro > 0 else amb.comprimento_paredes
            
            amb.comprimento_paredes = round(amb.comprimento_paredes, 2)
            amb.comprimento_vaos = round(amb.comprimento_vaos, 2)
            
            # Área Bruta = Perímetro * Pé Direito
            amb.area_bruta_parede = round(p * amb.pe_direito, 2)
            
            # Área de Vãos = Comprimento dos vãos * Altura padrão (2.10)
            amb.area_vaos = round(amb.comprimento_vaos * self.ALTURA_VAO_PADRAO, 2)
            
            # Área Líquida = Bruta - Vãos (nunca menor que zero)
            amb.area_liquida_parede = round(max(amb.area_bruta_parede - amb.area_vaos, 0), 2)
            
'''    def extrair_dados_reais(self) -> List[Ambiente]:
        if not self._loaded:
            return []

        # ---- 1. Agrupar textos por posição (x, y) ----
        grupos: Dict[Tuple[float, float], List[str]] = defaultdict(list)

        for entity in self.msp:
            # Pula entidades que não estão nas layers de texto
            if entity.dxf.layer.lower().strip() not in LAYERS_TEXTO:
                continue
            
            dxftype = entity.dxftype()
            if dxftype not in ('TEXT', 'MTEXT'):
                continue

            # O ezdxf já possui .plain_text() para MTEXT, o que evita ter que usar regex
            # para limpar as formatações malucas do AutoCAD (\pxqc; \W; etc)
            texto = entity.plain_text() if dxftype == 'MTEXT' else entity.dxf.text
            texto = texto.strip()
            
            if not texto:
                continue

            # Pega as coordenadas de inserção do texto
            x = round(entity.dxf.insert.x, 1)
            y = round(entity.dxf.insert.y, 1)
            grupos[(x, y)].append(texto)

        # ---- 2. Interpretar cada grupo como um ambiente ----
        NOMES_IGNORADOS = {'legenda', 'baixa', 'média', 'alta', 'existente', 'arquitetônico'}
        ambientes_dict: Dict[str, Ambiente] = {}

        for (x, y), textos in grupos.items():
            nome, area, perimetro, pe_direito = None, None, None, None

            for bloco in textos:
                for linha in bloco.split('\n'):
                    linha = linha.strip()
                    if re.match(r'^[\d,\.]+\s*m²$', linha):
                        area = self._parse_float_br(linha)
                    elif re.match(r'^P\s*=', linha, re.I):
                        perimetro = self._parse_float_br(linha)
                    elif re.match(r'^PD\s*=', linha, re.I):
                        pe_direito = self._parse_float_br(linha)
                    elif (nome is None and len(linha) >= 3 
                          and linha.lower() not in NOMES_IGNORADOS 
                          and not re.match(r'^[\d\(]', linha)):
                        nome = linha

            if nome and area is not None:
                if nome.upper() in ('CIRCU-', 'LAÇÃO'): nome = 'CIRCULAÇÃO'
                chave = f"{nome}|{area}"
                if chave not in ambientes_dict:
                    ambientes_dict[chave] = Ambiente(
                        nome=nome, area=area, 
                        perimetro=perimetro or 0.0, 
                        pe_direito=pe_direito or ALTURA_PADRAO,
                        cx=x, cy=y
                    )

        ambientes_lista = list(ambientes_dict.values())

        #Parte 1 Extreçao de dados?

        # ---- 3. Comprimentos geométricos (Enriquecimento) ----
        for entity in self.msp:
            layer = entity.dxf.layer.lower().strip()
            is_parede = layer in LAYERS_PAREDE
            is_vao = layer in LAYERS_VAO

            if not (is_parede or is_vao):
                continue

            comp = 0.0
            cx, cy = 0.0, 0.0
            dxftype = entity.dxftype()

            if dxftype == 'LINE':
                # Distância euclidiana nativa do Python entre início e fim
                comp = math.dist((entity.dxf.start.x, entity.dxf.start.y), 
                                 (entity.dxf.end.x, entity.dxf.end.y))
                cx = (entity.dxf.start.x + entity.dxf.end.x) / 2
                cy = (entity.dxf.start.y + entity.dxf.end.y) / 2

            elif dxftype == 'LWPOLYLINE':
                # Pega todos os vértices e soma as distâncias
                pontos = list(entity.vertices())
                if len(pontos) > 1:
                    comp = sum(math.dist(pontos[i][:2], pontos[i+1][:2]) for i in range(len(pontos)-1))
                    cx = sum(p[0] for p in pontos) / len(pontos)
                    cy = sum(p[1] for p in pontos) / len(pontos)

            if comp <= 0: continue

            # Normalizar unidade (caso o desenho esteja em milímetros ou centímetros)
            if comp > 1000: comp /= 1000
            elif comp > 100: comp /= 100

            # Associa a linha/parede ao texto do ambiente mais próximo
            melhor = min(ambientes_lista, key=lambda a: math.hypot(a.cx - cx, a.cy - cy), default=None)
            if melhor:
                if is_parede: melhor.comprimento_paredes += comp
                else: melhor.comprimento_vaos += comp

        # ---- 4. Calcular áreas de parede ----
        for amb in ambientes_lista:
            p = amb.perimetro if amb.perimetro > 0 else amb.comprimento_paredes
            amb.comprimento_paredes = round(amb.comprimento_paredes, 2)
            amb.comprimento_vaos = round(amb.comprimento_vaos, 2)
            amb.area_bruta_parede = round(p * amb.pe_direito, 2)
            amb.area_vaos = round(amb.comprimento_vaos * self.ALTURA_VAO_PADRAO, 2)
            amb.area_liquida_parede = round(max(amb.area_bruta_parede - amb.area_vaos, 0), 2)

        resultado = [a for a in ambientes_lista if not (a.perimetro <= 0 and a.area_bruta_parede > a.area * 50)]
        #parte 2 Calculo de Alvenaria?
        return sorted(resultado, key=lambda a: (a.nome, -a.area))'''