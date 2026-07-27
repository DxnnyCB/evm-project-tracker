from decimal import Decimal

from app.repositories import activity_repository, project_repository
from app.schemas.activity import ActivityCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def _create_activity(db_session: Session, project_id: int) -> None:
    activity_repository.create(
        db_session,
        project_id,
        ActivityCreate(
            name="Foundation work",
            bac=Decimal("10000"),
            planned_progress=Decimal("60"),
            actual_progress=Decimal("50"),
            ac=Decimal("4000"),
        ),
    )


def test_get_project_detail_returns_project_activities_and_consolidated(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Highway construction")
    _create_activity(db_session, project.id)

    response = client.get(f"/projects/{project.id}")

    assert response.status_code == 200
    body = response.json()

    assert body["id"] == project.id
    assert body["name"] == "Highway construction"
    assert len(body["activities"]) == 1

    activity = body["activities"][0]
    assert activity["name"] == "Foundation work"
    assert set(activity["indicators"]) == {
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
    assert Decimal(activity["indicators"]["pv"]) == Decimal("6000.00")
    assert Decimal(activity["indicators"]["ev"]) == Decimal("5000.00")

    consolidated = body["consolidated"]
    assert Decimal(consolidated["total_bac"]) == Decimal("10000.00")
    assert Decimal(consolidated["total_ev"]) == Decimal("5000.00")
    assert consolidated["cpi_status"] is not None


def test_get_project_detail_with_no_activities_returns_empty_list_and_none_indices(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Empty project")

    response = client.get(f"/projects/{project.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["activities"] == []
    assert body["consolidated"]["cpi"] is None
    assert body["consolidated"]["spi"] is None


def test_get_project_detail_returns_404_when_project_does_not_exist(client: TestClient) -> None:
    response = client.get("/projects/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}
