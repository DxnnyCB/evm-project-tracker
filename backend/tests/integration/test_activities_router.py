from decimal import Decimal

from app.repositories import activity_repository, project_repository
from app.schemas.activity import ActivityCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def _create_activity(db_session: Session, project_id: int):
    return activity_repository.create(
        db_session,
        project_id,
        ActivityCreate(
            name="Excavation",
            bac=Decimal("5000"),
            planned_progress=Decimal("40"),
            actual_progress=Decimal("30"),
            ac=Decimal("1200"),
        ),
    )


def test_get_activity_returns_activity_with_indicators(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Project")
    activity = _create_activity(db_session, project.id)

    response = client.get(f"/activities/{activity.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == activity.id
    assert body["project_id"] == project.id
    assert body["name"] == "Excavation"
    assert set(body["indicators"]) == {
        "pv",
        "ev",
        "cv",
        "sv",
        "cpi",
        "spi",
        "eac",
        "vac",
        "cpi_status",
        "cpi_message",
        "spi_status",
        "spi_message",
    }
    assert Decimal(body["indicators"]["pv"]) == Decimal("2000.00")
    assert Decimal(body["indicators"]["ev"]) == Decimal("1500.00")


def test_get_activity_returns_404_when_activity_does_not_exist(client: TestClient) -> None:
    response = client.get("/activities/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_update_activity_returns_200_with_updated_fields(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Project")
    activity = _create_activity(db_session, project.id)

    response = client.patch(f"/activities/{activity.id}", json={"actual_progress": "50"})

    assert response.status_code == 200
    body = response.json()
    assert Decimal(body["actual_progress"]) == Decimal("50.00")
    assert Decimal(body["bac"]) == Decimal("5000.00")


def test_update_activity_returns_404_when_activity_does_not_exist(client: TestClient) -> None:
    response = client.patch("/activities/999999", json={"actual_progress": "50"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_update_activity_returns_422_when_percentage_out_of_range(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Project")
    activity = _create_activity(db_session, project.id)

    response = client.patch(f"/activities/{activity.id}", json={"actual_progress": "150"})

    assert response.status_code == 422


def test_delete_activity_returns_204_and_activity_is_gone(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Project")
    activity = _create_activity(db_session, project.id)

    response = client.delete(f"/activities/{activity.id}")

    assert response.status_code == 204
    assert response.content == b""
    assert activity_repository.get_by_id(db_session, activity.id) is None


def test_delete_activity_returns_404_when_activity_does_not_exist(client: TestClient) -> None:
    response = client.delete("/activities/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
