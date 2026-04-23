from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Usando MySQL conforme configurado no alembic.ini
engine = create_engine('mysql+pymysql://root:fatec@localhost:3306/echocad', echo=True)
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