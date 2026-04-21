from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.upload import router as upload_router
from src.routes.especificacoes import router as especificacoes_router

app = FastAPI(
    title="EchoCAD API",
    description="API para extração de dados de plantas CAD e geração de documentação técnica.",
    version="1.0.0",
)

# Adiciona permissões para o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(especificacoes_router)


# Rota de boas vindas, indicando que está online.
@app.get('/')
async def root():
    """Rota de boas vindas, retorna uma mensagem
    indiciando que a api está online."""
    return {"message": "Welcome to EchoCad Api."}