import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.main import app
from src.database import get_session
from src.models.base import Base


@pytest.fixture(scope="session")
def test_engine():
    """Cria engine SQLite em memória para os testes."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=True
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def test_db(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    session.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(test_db):
    """Cria cliente de teste com dependência de DB injetada."""
    def override_get_session():
        yield test_db

    app.dependency_overrides[get_session] = override_get_session

    test_client = TestClient(app)

    yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def cleanup_uploads():
    """Fixture para cleanup automático de arquivos de teste."""
    files_to_cleanup = []

    yield files_to_cleanup

    for file_path in files_to_cleanup:
        if os.path.exists(file_path):
            os.remove(file_path)


@pytest.fixture
def dwg_file():
    """Fixture que retorna conteúdo de arquivo DWG de teste."""
    return b"conteudo fake do arquivo dwg"


@pytest.fixture
def pdf_file():
    """Fixture que retorna conteúdo de arquivo PDF de teste."""
    return b"%PDF-1.4 conteudo pdf"


@pytest.fixture
def dwf_file():
    """Fixture que retorna conteúdo de arquivo DWF de teste."""
    return b"DWF formato"


@pytest.fixture
def invalid_file():
    """Fixture que retorna conteúdo de arquivo inválido."""
    return b"conteudo invalido"
