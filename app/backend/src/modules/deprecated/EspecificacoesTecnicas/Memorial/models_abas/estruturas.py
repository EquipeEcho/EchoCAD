from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseDimensionItem


@dataclass
class SistemaVigaBaldrame(BaseDimensionItem):
    secao: Optional[str] = None
    lastro: Optional[float] = None
    concreto: Optional[float] = None
    ferragem: Optional[float] = None
    estribo: Optional[float] = None
    forma_em_madeira: Optional[float] = None


@dataclass
class EstacasBlocosCoroamento(BaseDimensionItem):
    valores_por_peca_l: Optional[float] = None
    valores_por_peca_h: Optional[float] = None
    valores_por_peca_c: Optional[float] = None
    lastro: Optional[float] = None
    concreto: Optional[float] = None
    ferragem: Optional[float] = None
    estribo: Optional[float] = None
    forma_em_madeira: Optional[float] = None


@dataclass
class Estruturas:
    sistema_viga_baldrame: List[SistemaVigaBaldrame] = field(default_factory=list)
    estacas_blocos_coroamento: List[EstacasBlocosCoroamento] = field(
        default_factory=list
    )
