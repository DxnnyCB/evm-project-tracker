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


def test_list_projects_returns_all_projects_without_indicators(
    client: TestClient, db_session: Session
) -> None:
    first = project_repository.create(db_session, "Highway construction")
    second = project_repository.create(db_session, "Bridge repair")

    response = client.get("/projects")

    assert response.status_code == 200
    body = response.json()
    assert body == [
        {"id": first.id, "name": "Highway construction"},
        {"id": second.id, "name": "Bridge repair"},
    ]


def test_list_projects_returns_empty_list_when_there_are_no_projects(
    client: TestClient,
) -> None:
    response = client.get("/projects")

    assert response.status_code == 200
    assert response.json() == []


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

    consolidated = body["consolidated"]
    assert Decimal(consolidated["total_bac"]) == Decimal("0")
    assert Decimal(consolidated["total_pv"]) == Decimal("0")
    assert Decimal(consolidated["total_ev"]) == Decimal("0")
    assert Decimal(consolidated["total_ac"]) == Decimal("0")
    assert Decimal(consolidated["cv"]) == Decimal("0")
    assert Decimal(consolidated["sv"]) == Decimal("0")
    assert consolidated["cpi"] is None
    assert consolidated["spi"] is None
    assert consolidated["eac"] is None
    assert consolidated["vac"] is None
    assert consolidated["cpi_status"] == "insufficient_data"
    assert consolidated["spi_status"] == "insufficient_data"
    assert consolidated["cpi_message"]
    assert consolidated["spi_message"]


def test_get_project_detail_returns_404_when_project_does_not_exist(client: TestClient) -> None:
    response = client.get("/projects/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_create_project_returns_201_with_created_project(client: TestClient) -> None:
    response = client.post("/projects", json={"name": "New highway"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "New highway"
    assert isinstance(body["id"], int)


def test_create_project_returns_422_when_name_is_missing(client: TestClient) -> None:
    response = client.post("/projects", json={})

    assert response.status_code == 422


def test_update_project_returns_200_with_updated_name(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Old name")

    response = client.patch(f"/projects/{project.id}", json={"name": "New name"})

    assert response.status_code == 200
    assert response.json() == {"id": project.id, "name": "New name"}


def test_update_project_returns_404_when_project_does_not_exist(client: TestClient) -> None:
    response = client.patch("/projects/999999", json={"name": "New name"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_delete_project_returns_204_and_project_is_gone(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "To be deleted")

    response = client.delete(f"/projects/{project.id}")

    assert response.status_code == 204
    assert response.content == b""
    assert project_repository.get_by_id(db_session, project.id) is None


def test_delete_project_returns_404_when_project_does_not_exist(client: TestClient) -> None:
    response = client.delete("/projects/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_create_activity_returns_201_with_created_activity(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Project with activities")

    response = client.post(
        f"/projects/{project.id}/activities",
        json={
            "name": "Excavation",
            "bac": "5000",
            "planned_progress": "40",
            "actual_progress": "30",
            "ac": "1200",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Excavation"
    assert body["project_id"] == project.id
    assert Decimal(body["bac"]) == Decimal("5000.00")


def test_create_activity_returns_404_when_project_does_not_exist(client: TestClient) -> None:
    response = client.post(
        "/projects/999999/activities",
        json={
            "name": "Excavation",
            "bac": "5000",
            "planned_progress": "40",
            "actual_progress": "30",
            "ac": "1200",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_create_activity_returns_422_when_bac_is_not_positive(
    client: TestClient, db_session: Session
) -> None:
    project = project_repository.create(db_session, "Project with invalid activity")

    response = client.post(
        f"/projects/{project.id}/activities",
        json={
            "name": "Excavation",
            "bac": "0",
            "planned_progress": "40",
            "actual_progress": "30",
            "ac": "1200",
        },
    )

    assert response.status_code == 422
