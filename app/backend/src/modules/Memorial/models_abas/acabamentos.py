from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseDimensionItem


@dataclass
class Pisos(BaseDimensionItem):
    placa_ceramica: Optional[str] = None


@dataclass
class Soleiras(BaseDimensionItem):
    pass


@dataclass
class Rodapes(BaseDimensionItem):
    pass


@dataclass
class AzulejosRodabancas(BaseDimensionItem):
    pass


@dataclass
class Peitoris(BaseDimensionItem):
    pass


@dataclass
class Forros(BaseDimensionItem):
    pass


@dataclass
class Acabamentos:
    pisos: List[Pisos] = field(default_factory=list)
    soleiras: List[Soleiras] = field(default_factory=list)
    rodapes: List[Rodapes] = field(default_factory=list)
    azulejos_rodabancas: List[AzulejosRodabancas] = field(default_factory=list)
    peitoris: List[Peitoris] = field(default_factory=list)
    forros: List[Forros] = field(default_factory=list)
