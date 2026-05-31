from deprecated import deprecated
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings

# criação do engine sincrono para alembic
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.echo_database,
    pool_pre_ping=True,
    pool_recycle=1800,  # recicla conexões a cada 30 min (antes do wait_timeout do MariaDB)
)
logger.debug(f"Database engine created with URL: {settings.DATABASE_URL}")

# criação do engine assíncrono para a aplicação
async_engine = create_async_engine(
    settings.DATABASE_ASYNC_URL,
    echo=settings.echo_database,
    pool_pre_ping=True,
    pool_recycle=1800,
)
logger.debug(f"Async database engine created with URL: {settings.DATABASE_ASYNC_URL}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session():
    """
    Gerador de sessão assíncrona para uso com FastAPI e SQLAlchemy.
    Este gerador é projetado para ser usado com dependências do FastAPI, garantindo
    que as sessões sejam corretamente gerenciadas e fechadas após o uso.
    Ele utiliza o AsyncSession do SQLAlchemy para operações assíncronas,
    permitindo melhor desempenho e escalabilidade em aplicações web.
    Em caso de erros durante as operações de banco de dados, a sessão será
    revertida para evitar inconsistências, e o erro será registrado usando o loguru.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database error: {}", e)
            raise


@deprecated(
    reason="Use get_async_session instead for better performance and scalability."
)
def get_session():
    """
    Gerador de sessão síncrona para uso com FastAPI e SQLAlchemy.
    Este gerador é projetado para ser usado com dependências do FastAPI, garantindo
    que as sessões sejam corretamente gerenciadas e fechadas após o uso.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logger.error("Database error: {}", e)
        raise
    finally:
        session.close()
