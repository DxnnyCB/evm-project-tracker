from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.project import Project
from app.repositories import activity_repository, project_repository
from app.schemas.activity import (
    ActivityCreate,
    ActivityIndicatorsSchema,
    ActivityRead,
    ActivityWithIndicators,
)
from app.schemas.project import (
    ProjectConsolidatedIndicatorsSchema,
    ProjectCreate,
    ProjectDetail,
    ProjectRead,
    ProjectUpdate,
)
from app.services.evm.indicators import (
    ActivityInput,
    calculate_activity_indicators,
    calculate_project_consolidated,
)

router = APIRouter(prefix="/projects", tags=["projects"])

PROJECT_NOT_FOUND_RESPONSE = {status.HTTP_404_NOT_FOUND: {"description": "Project not found"}}


def _get_project_or_404(db: Session, project_id: int) -> Project:
    project = project_repository.get_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    """Crea un proyecto nuevo."""
    project = project_repository.create(db, data.name)
    return ProjectRead.model_validate(project)


@router.get("", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRead]:
    """Listado liviano de proyectos, sin calcular indicadores EVM."""
    projects = project_repository.list_all(db)
    return [ProjectRead.model_validate(project) for project in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectDetail,
    responses=PROJECT_NOT_FOUND_RESPONSE,
)
def get_project_detail(project_id: int, db: Session = Depends(get_db)) -> ProjectDetail:
    """Proyecto + actividades (cada una con sus 8 indicadores EVM) + consolidado."""
    project = _get_project_or_404(db, project_id)
    activities = activity_repository.list_by_project(db, project_id)

    activities_with_indicators = [
        ActivityWithIndicators(
            id=activity.id,
            project_id=activity.project_id,
            name=activity.name,
            bac=activity.bac,
            planned_progress=activity.planned_progress,
            actual_progress=activity.actual_progress,
            ac=activity.ac,
            indicators=ActivityIndicatorsSchema.from_domain(
                calculate_activity_indicators(
                    activity.bac,
                    activity.planned_progress,
                    activity.actual_progress,
                    activity.ac,
                )
            ),
        )
        for activity in activities
    ]

    consolidated = calculate_project_consolidated(
        [
            ActivityInput(
                bac=activity.bac,
                planned_progress=activity.planned_progress,
                actual_progress=activity.actual_progress,
                ac=activity.ac,
            )
            for activity in activities
        ]
    )

    return ProjectDetail(
        id=project.id,
        name=project.name,
        activities=activities_with_indicators,
        consolidated=ProjectConsolidatedIndicatorsSchema.from_domain(consolidated),
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
    responses=PROJECT_NOT_FOUND_RESPONSE,
)
def update_project(
    project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)
) -> ProjectRead:
    """Actualiza el nombre del proyecto (parcial)."""
    project = _get_project_or_404(db, project_id)
    project = project_repository.update(db, project, data.name)
    return ProjectRead.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=PROJECT_NOT_FOUND_RESPONSE,
)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    """Elimina el proyecto (CASCADE elimina sus actividades)."""
    project = _get_project_or_404(db, project_id)
    project_repository.delete(db, project)


@router.post(
    "/{project_id}/activities",
    response_model=ActivityRead,
    status_code=status.HTTP_201_CREATED,
    responses=PROJECT_NOT_FOUND_RESPONSE,
)
def create_activity(
    project_id: int, data: ActivityCreate, db: Session = Depends(get_db)
) -> ActivityRead:
    """Crea una actividad dentro de un proyecto existente."""
    _get_project_or_404(db, project_id)
    activity = activity_repository.create(db, project_id, data)
    return ActivityRead.model_validate(activity)
