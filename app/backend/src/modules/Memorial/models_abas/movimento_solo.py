from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BaseSoloEntry:
    ambiente: Optional[str] = None
    tipo: Optional[str] = None
    i_pct: Optional[float] = None
    l_m: Optional[float] = None
    c_m: Optional[float] = None
    h_m: Optional[float] = None
    lastro_m: Optional[float] = None
    area_m2: Optional[float] = None
    volume_m3: Optional[float] = None


@dataclass
class EscavacaoItem(BaseSoloEntry):
    """2.2 Escavações"""
    pass


@dataclass
class AterroReaterroItem(BaseSoloEntry):
    """2.3 Aterros e Reaterros"""
    pass


@dataclass
class EnrocamentoItem(BaseSoloEntry):
    """2.4 Enrocamentos"""
    pass


@dataclass
class ContencaoItem(BaseSoloEntry):
    """2.5 Contenções"""
    pass


@dataclass
class TaludamentoItem(BaseSoloEntry):
    """2.6 Taludamentos"""
    pass


@dataclass
class NivelamentoCompactacaoItem(BaseSoloEntry):
    """2.7 Nivelamentos e Compactações do Terreno"""
    pass


@dataclass
class MovimentoSolo:
    """Agregador para as seções de Movimento de Solo do levantamento.
    Cada lista representa as linhas (ambientes) da respectiva tabela no Excel.
    """
    escavacoes: List[EscavacaoItem] = field(default_factory=list)
    aterros: List[AterroReaterroItem] = field(default_factory=list)
    enrocamentos: List[EnrocamentoItem] = field(default_factory=list)
    contencoes: List[ContencaoItem] = field(default_factory=list)
    taludamentos: List[TaludamentoItem] = field(default_factory=list)
    nivelamentos: List[NivelamentoCompactacaoItem] = field(default_factory=list)
