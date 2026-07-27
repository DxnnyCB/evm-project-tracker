from collections.abc import Generator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from app.core.database import engine, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

BACKEND_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> None:
    """Aplica las migraciones de Alembic contra la DB de `DATABASE_URL` antes
    de correr la suite. Usa la misma base de datos de desarrollo (por decisión
    explícita: es un ejercicio técnico, no hay datos reales en juego) y
    corre `alembic upgrade head` en vez de `Base.metadata.create_all()`, para
    que una migración rota se detecte en los tests en lugar de notarse después.
    """
    alembic_cfg = Config(str(BACKEND_ROOT / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Sesión de test atada a una única conexión/transacción externa.

    Los repositories solo hacen `flush()` (nunca `commit()`), así que todo lo
    que ocurre durante el test queda dentro de esta transacción y se revierte
    al final con `rollback()` — sin residuos en la base de datos compartida
    con desarrollo, sin necesidad de SAVEPOINTs anidados.
    """
    connection = engine.connect()
    transaction = connection.begin()
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = testing_session_local()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Cliente de FastAPI con `get_db` sobreescrito para usar `db_session`."""

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
