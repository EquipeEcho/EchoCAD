from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseDimensionItem


@dataclass
class Paineis(BaseDimensionItem):
    categoria: Optional[str] = None
    material: Optional[str] = None


@dataclass
class VergasContraVergas(BaseDimensionItem):
    qtd: Optional[int] = None
    verga: Optional[float] = None
    c_verga: Optional[float] = None
    engastamento: Optional[str] = None


@dataclass
class GuiasCalcadasPasseios(BaseDimensionItem):
    pass


@dataclass
class Alvenarias:
    paineis: List[Paineis] = field(default_factory=list)
    vergas_contra_vergas: List[VergasContraVergas] = field(default_factory=list)
    guias_calcadas_passeios: List[GuiasCalcadasPasseios] = field(default_factory=list)
