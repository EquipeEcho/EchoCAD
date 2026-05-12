from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

# Usando MySQL conforme configurado no alembic.ini
engine = create_engine(settings.database_url, echo=settings.echo_database, pool_pre_ping=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logger.error('Database error: {}', e)
        raise
    finally:
        session.close()
