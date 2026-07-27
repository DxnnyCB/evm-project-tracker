from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.project import Project

ACTIVITY_NAME_MAX_LENGTH = 200
MONEY_PRECISION = 14
MONEY_SCALE = 2
PERCENTAGE_PRECISION = 5
PERCENTAGE_SCALE = 2
MIN_PERCENTAGE = 0
MAX_PERCENTAGE = 100


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("bac > 0", name="bac_positive"),
        CheckConstraint("ac >= 0", name="ac_non_negative"),
        CheckConstraint(
            f"planned_progress BETWEEN {MIN_PERCENTAGE} AND {MAX_PERCENTAGE}",
            name="planned_progress_within_range",
        ),
        CheckConstraint(
            f"actual_progress BETWEEN {MIN_PERCENTAGE} AND {MAX_PERCENTAGE}",
            name="actual_progress_within_range",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(ACTIVITY_NAME_MAX_LENGTH), nullable=False)
    bac: Mapped[Decimal] = mapped_column(Numeric(MONEY_PRECISION, MONEY_SCALE), nullable=False)
    planned_progress: Mapped[Decimal] = mapped_column(
        Numeric(PERCENTAGE_PRECISION, PERCENTAGE_SCALE), nullable=False
    )
    actual_progress: Mapped[Decimal] = mapped_column(
        Numeric(PERCENTAGE_PRECISION, PERCENTAGE_SCALE), nullable=False
    )
    ac: Mapped[Decimal] = mapped_column(Numeric(MONEY_PRECISION, MONEY_SCALE), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    project: Mapped["Project"] = relationship(back_populates="activities")
