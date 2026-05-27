from deprecated import deprecated
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings

# Usando MariaDB conforme configurado no alembic.ini
engine = create_engine(
    settings.DATABASE_URL, echo=settings.echo_database, pool_pre_ping=True
)

async_engine = create_async_engine(
    settings.DATABASE_ASYNC_URL, echo=settings.echo_database, pool_pre_ping=True
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session():
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
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logger.error("Database error: {}", e)
        raise
    finally:
        session.close()
