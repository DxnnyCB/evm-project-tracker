from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

engine = create_engine(get_settings().database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Convención de nombres para que Alembic autogenere constraints con nombres
# predecibles (necesario para poder revertir migraciones de forma confiable).
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(constraint_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base declarativa compartida por todos los modelos SQLAlchemy."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: entrega una sesión de DB por request.

    Hace commit al final si la request no lanzó ninguna excepción, o rollback
    si la lanzó. Los repositories nunca hacen commit por sí mismos (solo
    flush) — el commit es responsabilidad exclusiva de esta unidad de trabajo
    por request, para que los tests de integración puedan envolver toda la
    request en una transacción externa y revertirla sin residuos.

    Importante: debe inyectarse con ``scope="function"`` (ver ``DbSession``).
    Con el scope por defecto (``"request"``), FastAPI ejecuta el código
    posterior al ``yield`` *después* de enviar la respuesta HTTP, así que un
    201 podría llegar al cliente antes del ``commit`` y un GET inmediato no
    vería el recurso recién creado.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Inyección estándar: commit centralizado en get_db, pero *antes* de responder.
DbSession = Annotated[Session, Depends(get_db, scope="function")]
