from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import activity_repository, project_repository
from app.schemas.activity import ActivityIndicatorsSchema, ActivityWithIndicators
from app.schemas.project import ProjectConsolidatedIndicatorsSchema, ProjectDetail
from app.services.evm.indicators import (
    ActivityInput,
    calculate_activity_indicators,
    calculate_project_consolidated,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project_detail(project_id: int, db: Session = Depends(get_db)) -> ProjectDetail:
    """Proyecto + actividades (cada una con sus 8 indicadores EVM) + consolidado."""
    project = project_repository.get_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

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
