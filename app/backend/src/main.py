from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.routes.router_upload import router as upload_router
from src.routes.router_project import router as projeto_router
from src.routes.router_blueprints import router as planta_router
from src.routes.router_standards import router as norma_router
from src.routes.deprecated.download import router as download_router

app = FastAPI(
    title="EchoCAD API",
    description="API para extração de dados de plantas CAD e geração de documentação técnica.",
    version="1.1.0",
)

# Adiciona permissões para o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas de criação de objetos
app.include_router(upload_router)
app.include_router(projeto_router)
app.include_router(planta_router)
app.include_router(norma_router)

# TODO: reconstruir depois de implantado logica de IA
# rotas de processamento e download
# obs. precisa de teste
# app.include_router(especificacoes_router)
# app.include_router(processamento_router)
# app.include_router(download_router)
# app.include_router(agent_test_router)


@app.get('/', status_code=status.HTTP_200_OK)
async def root():
    """Rota de boas vindas, retorna uma mensagem
    indiciando que a api está online."""
    return {"message": "Welcome to EchoCad Api."}
