from .usuario import router as usuario_router
from .projeto import router as projeto_router
from .norma import router as norma_router
from .planta_cad import router as planta_cad_router
from .especificacao_tecnica import router as especificacao_tecnica_router
from .memorial_calculo import router as memorial_calculo_router

__all__ = [
    'usuario_router',
    'projeto_router',
    'norma_router',
    'planta_cad_router',
    'especificacao_tecnica_router',
    'memorial_calculo_router'
]