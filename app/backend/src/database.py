from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

# Usando MySQL conforme configurado no alembic.ini
engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
