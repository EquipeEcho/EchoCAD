from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .alvenarias import Paineis


@dataclass
class DimensaoItem:
    c: Optional[float] = None
    l: Optional[float] = None
    h: Optional[float] = None
    e: Optional[float] = None
    a: Optional[float] = None
    nota: Optional[str] = None


@dataclass
class VaoItem:
    tipo: Optional[str] = None
    c: Optional[float] = None
    h: Optional[float] = None
    e: Optional[float] = None
    a: Optional[float] = None
    nota: Optional[str] = None


@dataclass
class AlvenariaAdicionalItem:
    tipo: Optional[str] = None
    c: Optional[float] = None
    h: Optional[float] = None
    e: Optional[float] = None
    a: Optional[float] = None
    v: Optional[float] = None
    nota: Optional[str] = None


@dataclass
class TabelaARegistro:
    """Tabela A: Dimensões | Vãos | Alvenarias Adicionais
    - `ambiente` representa a linha (o ambiente onde as medidas foram tomadas)
    - `dimensoes` lista os blocos com C, L, h, e, A
    - `vaos` lista os vãos (Tipo, C, h, e, A)
    - `alvenarias_adicionais` lista alvenarias adicionais (Tipo, C, h, e, A, V)
    """
    ambiente: Optional[str] = None
    dimensoes: List[DimensaoItem] = field(default_factory=list)
    vaos: List[VaoItem] = field(default_factory=list)
    alvenarias_adicionais: List[AlvenariaAdicionalItem] = field(default_factory=list)


@dataclass
class PilarItem:
    ambiente: Optional[str] = None
    peca: Optional[str] = None
    c: Optional[float] = None
    l: Optional[float] = None
    h: Optional[float] = None
    a: Optional[float] = None
    nota: Optional[str] = None


@dataclass
class VigaItemTabelaB:
    ambiente: Optional[str] = None
    peca: Optional[str] = None
    c: Optional[float] = None
    l: Optional[float] = None
    h: Optional[float] = None
    e: Optional[float] = None
    a: Optional[float] = None
    nota: Optional[str] = None


@dataclass
class LajeItem:
    ambiente: Optional[str] = None
    peca: Optional[str] = None
    c: Optional[float] = None
    l: Optional[float] = None
    e: Optional[float] = None
    a: Optional[float] = None
    nota: Optional[str] = None


@dataclass
class TabelaBRegistro:
    """Tabela B: Pilar | Viga | Laje"""
    ambiente: Optional[str] = None
    pilares: List[PilarItem] = field(default_factory=list)
    vigas: List[VigaItemTabelaB] = field(default_factory=list)
    lajes: List[LajeItem] = field(default_factory=list)


@dataclass
class TabelaCRegistro:
    """Tabela C: Quadros / Conduletes / Tomadas / Interruptores / Luminárias / Dutos / Cabos / Acessórios / Equipamentos"""
    ambiente: Optional[str] = None
    quadros: Optional[int] = None
    conduletes: Optional[int] = None
    tomadas: Optional[int] = None
    interruptores: Optional[int] = None
    luminarias: Optional[int] = None
    dutos_m: Optional[float] = None
    cabos_m: Optional[float] = None
    acessorios: Optional[int] = None
    equipamentos_tipo: Optional[str] = None
    equipamentos_qtd: Optional[int] = None


@dataclass
class AguaFriaItem:
    ambiente: Optional[str] = None
    cavalete: Optional[int] = None
    reservatorio_tipo: Optional[str] = None
    registros: Optional[int] = None
    valvulas: Optional[int] = None
    dutos_m: Optional[float] = None
    caixas_qtd: Optional[int] = None
    drenagem_qtd: Optional[int] = None


@dataclass
class AguaPluvialItem:
    ambiente: Optional[str] = None
    calhas_tipo: Optional[str] = None
    dutos_m: Optional[float] = None
    caixas_qtd: Optional[int] = None


@dataclass
class EsgotoItem:
    ambiente: Optional[str] = None
    dutos_m: Optional[float] = None
    caixas_qtd: Optional[int] = None


@dataclass
class TabelaDRegistro:
    """Tabela D: Água Fria/Quente/Reúso | Água Pluvial | Esgoto"""
    ambiente: Optional[str] = None
    agua_fria: List[AguaFriaItem] = field(default_factory=list)
    agua_pluvial: List[AguaPluvialItem] = field(default_factory=list)
    esgoto: List[EsgotoItem] = field(default_factory=list)


@dataclass
class RedeRegistro:
    ambiente: Optional[str] = None
    quadros: Optional[int] = None
    conduletes: Optional[int] = None
    tomadas: Optional[int] = None
    dutos_m: Optional[float] = None
    cabos_m: Optional[float] = None


@dataclass
class SPDARegistro:
    ambiente: Optional[str] = None
    captacao_tipo: Optional[str] = None
    condulete_m: Optional[float] = None
    dutos_m: Optional[float] = None
    cabos_m: Optional[float] = None


@dataclass
class TabelaFRegistro:
    """Tabela F: Rede | SPDA (vista geral por ambiente)"""
    ambiente: Optional[str] = None
    rede: List[RedeRegistro] = field(default_factory=list)
    spda: List[SPDARegistro] = field(default_factory=list)


@dataclass
class ContraIncendioItem:
    ambiente: Optional[str] = None
    reservatorio_tipo: Optional[str] = None
    registros: Optional[int] = None
    valvulas: Optional[int] = None
    dutos_m: Optional[float] = None
    hidrantes_qtd: Optional[int] = None


@dataclass
class InstPressurizadaItem:
    ambiente: Optional[str] = None
    reservatorio_tipo: Optional[str] = None
    registros: Optional[int] = None
    valvulas: Optional[int] = None
    dutos_m: Optional[float] = None
    reguladores_qtd: Optional[int] = None


@dataclass
class TabelaGRegistro:
    """Tabela G: Contra-incêndio | Instalações Pressurizadas"""
    ambiente: Optional[str] = None
    contra_incendio: List[ContraIncendioItem] = field(default_factory=list)
    instalacoes_pressurizadas: List[InstPressurizadaItem] = field(default_factory=list)


@dataclass
class LevantamentoCampo:
    """Classe principal que agrega todas as tabelas A..G do levantamento de campo.
    Cada atributo representa as linhas/entradas da respectiva tabela no template Excel.
    """
    tabela_a: List[TabelaARegistro] = field(default_factory=list)
    tabela_b: List[TabelaBRegistro] = field(default_factory=list)
    tabela_c: List[TabelaCRegistro] = field(default_factory=list)
    tabela_d: List[TabelaDRegistro] = field(default_factory=list)
    tabela_f: List[TabelaFRegistro] = field(default_factory=list)
    tabela_g: List[TabelaGRegistro] = field(default_factory=list)
    paineis: List[Paineis] = field(default_factory=list)
