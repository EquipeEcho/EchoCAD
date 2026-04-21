from fastapi import APIRouter
from .database import (
    usuario_router,
    projeto_router,
    comando_ia_router,
    documento_gerado_router,
    especificacao_tecnica_router,
    calculo_router,
    memorial_calculo_router,
    elemento_router,
    arquivo_router,
    coordenada_router,
    processamento_router
)

router = APIRouter()

# Este arquivo é responsável por incluir todas as rotas relacionadas ao banco de dados, organizando-as em um único lugar para facilitar a manutenção e a escalabilidade do projeto.
# Cada rota específica (como criação de usuário, projeto, comando IA, etc.) é importada dos seus respectivos módulos e incluída no router principal com um prefixo adequado.
router.include_router(usuario_router, prefix='/usuario')
router.include_router(projeto_router, prefix='/projeto')
router.include_router(comando_ia_router, prefix='/comando_ia')
router.include_router(documento_gerado_router, prefix='/documento_gerado')
router.include_router(especificacao_tecnica_router, prefix='/especificacao_tecnica')
router.include_router(calculo_router, prefix='/calculo')
router.include_router(memorial_calculo_router, prefix='/memorial_calculo')
router.include_router(elemento_router, prefix='/elemento')
router.include_router(arquivo_router, prefix='/arquivo')
router.include_router(coordenada_router, prefix='/coordenada')
router.include_router(processamento_router, prefix='/processamento')