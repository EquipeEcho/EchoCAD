from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseDimensionItem:
    ambiente: Optional[str] = None
    peca: Optional[str] = None
    tipo: Optional[str] = None
    c: Optional[float] = None
    l: Optional[float] = None
    h: Optional[float] = None
    e: Optional[float] = None
    a: Optional[float] = None
    vaos: Optional[float] = None
    verga: Optional[float] = None
    qtd: Optional[float] = None
    total: Optional[float] = None
    nota: Optional[str] = None
