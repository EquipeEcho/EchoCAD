from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class ComunicacoesAmbientais:
    ambiente: Optional[str] = None
    local: Optional[str] = None
    saida: Optional[str] = None
    extintor: Optional[int] = None
    quadro_forca: Optional[int] = None
    hidrante: Optional[int] = None
    alarme: Optional[int] = None
    proibido_fumar: Optional[int] = None
    perigo_inflamavel: Optional[int] = None
    risco_explosao: Optional[int] = None
    contra_mao: Optional[int] = None
    curva_direita: Optional[int] = None
    curva_esquerda: Optional[int] = None
    velocidade_40: Optional[int] = None
    pare: Optional[int] = None
