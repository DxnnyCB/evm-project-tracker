from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


def get_by_id(db: Session, activity_id: int) -> Activity | None:
    return db.get(Activity, activity_id)


def list_by_project(db: Session, project_id: int) -> list[Activity]:
    stmt = select(Activity).where(Activity.project_id == project_id).order_by(Activity.id)
    return list(db.scalars(stmt).all())


def create(db: Session, project_id: int, data: ActivityCreate) -> Activity:
    activity = Activity(project_id=project_id, **data.model_dump())
    db.add(activity)
    db.flush()
    return activity


def update(db: Session, activity: Activity, data: ActivityUpdate) -> Activity:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(activity, field, value)
    if updates:
        db.flush()
    return activity


def delete(db: Session, activity: Activity) -> None:
    db.delete(activity)
    db.flush()
