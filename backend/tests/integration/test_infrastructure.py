"""Pruebas de la infraestructura de tests de integración en sí misma:
confirman que las migraciones de Alembic se aplicaron, que el cliente puede
llegar a la API, y que el rollback por test aísla los datos sin dejar
residuos en la base de datos compartida con desarrollo.
"""

from app.repositories import project_repository
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_health_endpoint_is_reachable_through_the_test_client(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_creating_a_project_is_visible_within_the_same_test(db_session: Session) -> None:
    project = project_repository.create(db_session, "Rollback isolation project")

    assert project.id is not None
    assert project_repository.get_by_id(db_session, project.id) is not None


def test_project_created_in_previous_test_did_not_leak(db_session: Session) -> None:
    """Depende de correrse después del test anterior (mismo orden de archivo).

    Si el rollback no funcionara, esta lista contendría el proyecto creado en
    `test_creating_a_project_is_visible_within_the_same_test`.
    """
    projects = [p.name for p in project_repository.list_all(db_session)]

    assert "Rollback isolation project" not in projects
