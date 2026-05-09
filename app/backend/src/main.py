from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.routes.router_upload import router as upload_router
from src.routes.router_project import router as projeto_router
from src.routes.router_blueprints import router as planta_router
from src.routes.router_standards import router as norma_router

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

# rotas de manipulação dos objetos
app.include_router(upload_router)
app.include_router(projeto_router)
app.include_router(planta_router)
app.include_router(norma_router)


@app.get('/', status_code=status.HTTP_200_OK, tags=['root'], summary='Rota de boas vindas')
async def root():
    """Rota de boas vindas, retorna uma mensagem indicando que a api está online."""
    return {"message": "Welcome to EchoCad Api."}
