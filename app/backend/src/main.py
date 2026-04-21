from fastapi import FastAPI
from src.routes.upload import router
from src.routes.route_database import router as database_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adiciona permissões para o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(database_router)


# Rota de boas vindas, indicando que está online.
@app.get('/')
async def root():
    """Rota de boas vindas, retorna uma mensagem
    indiciando que a api está online."""
    return {"message": "Welcome to EchoCad Api."}
