from fastapi import APIRouter
from .database import (
    usuario_router,
    norma_router,
    planta_cad_router,
    especificacao_tecnica_router,
    memorial_calculo_router,
)

router = APIRouter()

# Este arquivo é responsável por incluir todas as rotas relacionadas
# ao banco de dados, organizando-as em um único lugar para facilitar
# a manutenção e a escalabilidade do projeto.
# Cada rota específica (como criação de usuário, projeto, comando IA, etc.)
# é importada dos seus respectivos módulos e incluída no router principal
# com um prefixo adequado.

router.include_router(usuario_router, prefix='/usuario')
router.include_router(norma_router, prefix='/norma')
router.include_router(planta_cad_router, prefix='/planta_cad')
router.include_router(especificacao_tecnica_router, prefix='/especificacao_tecnica')
router.include_router(memorial_calculo_router, prefix='/memorial_calculo')
