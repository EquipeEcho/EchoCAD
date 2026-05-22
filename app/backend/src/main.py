from loguru import logger
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routes.router_blueprints import router as planta_router
from src.routes.router_project import router as projeto_router
from src.routes.router_processing import memorial_router, router as processing_router
from src.routes.router_standards import router as norma_router
from src.routes.router_upload import router as upload_router
from src.routes.router_users import router as users_router

logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.LOG_LEVEL,
    backtrace=True,
    diagnose=True,
)

# TODO: debugging / desabilitar em prod
logger.debug("Configuracoes carregadas: {}", settings.model_dump_json(indent=4))

app = FastAPI(
    title="EchoCAD API",
    description="API para extracao de dados de plantas CAD e geracao de documentacao tecnica.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(projeto_router)
app.include_router(planta_router)
app.include_router(processing_router)
app.include_router(memorial_router)
app.include_router(norma_router)
app.include_router(users_router)


@app.get(
    "/", status_code=status.HTTP_200_OK, tags=["root"], summary="Rota de boas vindas"
)
async def root():
    logger.debug("Rota de boas vindas acessada.")
    return {"message": "Welcome to EchoCad Api."}
