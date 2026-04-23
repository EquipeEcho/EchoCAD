from .usuario import router as usuario_router
from .projeto import router as projeto_router
from .comando_ia import router as comando_ia_router
from .documento_gerado import router as documento_gerado_router
from .especificacao_tecnica import router as especificacao_tecnica_router
from .calculo import router as calculo_router
from .memorial_calculo import router as memorial_calculo_router
from .elemento import router as elemento_router
from .arquivo import router as arquivo_router
from .coordenada import router as coordenada_router
from .processamento import router as processamento_router

__all__ = [
    'usuario_router',
    'projeto_router',
    'comando_ia_router',
    'documento_gerado_router',
    'especificacao_tecnica_router',
    'calculo_router',
    'memorial_calculo_router',
    'elemento_router',
    'arquivo_router',
    'coordenada_router',
    'processamento_router'
]