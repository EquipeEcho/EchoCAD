from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class InterdicaoItem:
    fase: Optional[str] = None
    ambiente: Optional[str] = None
    local: Optional[str] = None


@dataclass
class EletricaItem:
    condulete: Optional[float] = None
    tomadas: Optional[int] = None
    interruptores: Optional[int] = None
    luminarias: Optional[int] = None
    dutos: Optional[float] = None
    cabos: Optional[float] = None
    captacao: Optional[str] = None
    aterramento: Optional[float] = None
    quadros: Optional[int] = None
    postes: Optional[int] = None


@dataclass
class AguaItem:
    cavalete: Optional[int] = None
    reservatorio: Optional[str] = None
    registros: Optional[int] = None
    valvulas: Optional[int] = None
    torneiras: Optional[int] = None
    dutos: Optional[float] = None
    calhas: Optional[str] = None
    caixas: Optional[int] = None
    drenos: Optional[int] = None


@dataclass
class EsquadriasItem:
    portas: Optional[int] = None
    janelas: Optional[int] = None


@dataclass
class TelhadosItem:
    telha: Optional[str] = None
    trama: Optional[float] = None
    tesoura: Optional[int] = None


@dataclass
class EquipamentoItem:
    item: Optional[str] = None
    qtd: Optional[int] = None


@dataclass
class AlvenariaItem:
    tipo: Optional[str] = None
    v: Optional[float] = None


@dataclass
class EstruturaItem:
    fundacao: Optional[float] = None
    pilar: Optional[float] = None
    viga: Optional[float] = None
    laje: Optional[float] = None


@dataclass
class DemolicaoItem:
    ambiente: Optional[str] = None
    piso: Optional[float] = None
    rodape: Optional[float] = None
    azulejo: Optional[float] = None
    forro: Optional[float] = None
    alvenaria: Optional[AlvenariaItem] = None
    estrutura: Optional[EstruturaItem] = None


@dataclass
class ServicosPreliminares:
    interdicoes: List[InterdicaoItem] = field(default_factory=list)
    remocoes: List[dict] = field(default_factory=list)
    demolicoes: List[DemolicaoItem] = field(default_factory=list)

