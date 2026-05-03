from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import BaseDimensionItem

@dataclass
class InstEletricas:
    local: Optional[str] = None
    circuito: Optional[str] = None
    qtd_cabos: Optional[float] = None
    cabo_especificacao: Optional[str] = None
    postes: Optional[int] = None
    cruzetas: Optional[int] = None
    suportes: Optional[int] = None
    isoladores: Optional[int] = None

@dataclass
class InstTelefoniaRede:
    local: Optional[str] = None
    circuito: Optional[str] = None
    rede: Optional[str] = None
    patch_cord: Optional[str] = None
    camera: Optional[int] = None
    tv: Optional[int] = None
    telefonia: Optional[int] = None
    eletrocalha: Optional[int] = None
    duto_l: Optional[float] = None
    duto_h: Optional[float] = None
    duto_c: Optional[float] = None
    e_tomadas: Optional[int] = None

@dataclass
class InstMecanicas(BaseDimensionItem):
    pot: Optional[str] = None
    mat_complementar: Optional[str] = None
    dutos: Optional[float] = None
    cabo_eletrico: Optional[float] = None
    gas_refrig: Optional[str] = None

@dataclass
class InstPressurizadas(BaseDimensionItem):
    tipo: Optional[str] = None
    dutos_dn: Optional[float] = None
    dutos_h: Optional[float] = None
    dutos_c: Optional[float] = None
    reguladores_qtd: Optional[int] = None
    valvulas_qtd: Optional[int] = None
    registros_qtd: Optional[int] = None
    reservatorios_tipo: Optional[str] = None

@dataclass
class InstSeguranca(BaseDimensionItem):
    hidrantes: Optional[int] = None
    extintores: Optional[int] = None
    aterramento: Optional[str] = None
    caixas_inspecao: Optional[int] = None
    registro_vazao: Optional[float] = None
