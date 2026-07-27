from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


def get_by_id(db: Session, project_id: int) -> Project | None:
    return db.get(Project, project_id)


def list_all(db: Session) -> list[Project]:
    return list(db.scalars(select(Project).order_by(Project.id)).all())


def create(db: Session, name: str) -> Project:
    project = Project(name=name)
    db.add(project)
    db.flush()
    return project


def update(db: Session, project: Project, name: str | None) -> Project:
    if name is not None:
        project.name = name
        db.flush()
    return project


def delete(db: Session, project: Project) -> None:
    db.delete(project)
    db.flush()
