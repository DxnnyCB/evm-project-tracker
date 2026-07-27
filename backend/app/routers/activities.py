from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.activity import Activity
from app.repositories import activity_repository
from app.schemas.activity import (
    ActivityIndicatorsSchema,
    ActivityRead,
    ActivityUpdate,
    ActivityWithIndicators,
)
from app.services.evm.indicators import calculate_activity_indicators

router = APIRouter(prefix="/activities", tags=["activities"])

ACTIVITY_NOT_FOUND_RESPONSE = {status.HTTP_404_NOT_FOUND: {"description": "Activity not found"}}


def _get_activity_or_404(db: Session, activity_id: int) -> Activity:
    activity = activity_repository.get_by_id(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return activity


@router.get(
    "/{activity_id}",
    response_model=ActivityWithIndicators,
    responses=ACTIVITY_NOT_FOUND_RESPONSE,
)
def get_activity(activity_id: int, db: Session = Depends(get_db)) -> ActivityWithIndicators:
    """Actividad + sus 8 indicadores EVM."""
    activity = _get_activity_or_404(db, activity_id)

    return ActivityWithIndicators(
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


@router.patch(
    "/{activity_id}",
    response_model=ActivityRead,
    responses=ACTIVITY_NOT_FOUND_RESPONSE,
)
def update_activity(
    activity_id: int, data: ActivityUpdate, db: Session = Depends(get_db)
) -> ActivityRead:
    """Actualiza una actividad (parcial: solo los campos enviados)."""
    activity = _get_activity_or_404(db, activity_id)
    activity = activity_repository.update(db, activity, data)
    return ActivityRead.model_validate(activity)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ACTIVITY_NOT_FOUND_RESPONSE,
)
def delete_activity(activity_id: int, db: Session = Depends(get_db)) -> None:
    """Elimina una actividad."""
    activity = _get_activity_or_404(db, activity_id)
    activity_repository.delete(db, activity)
