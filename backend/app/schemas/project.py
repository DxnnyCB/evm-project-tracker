from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.activity import ActivityWithIndicators
from app.services.evm.enums import CpiStatus, SpiStatus

PROJECT_NAME_MAX_LENGTH = 200


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=PROJECT_NAME_MAX_LENGTH)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=PROJECT_NAME_MAX_LENGTH)


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProjectConsolidatedIndicatorsSchema(BaseModel):
    total_bac: Decimal
    total_pv: Decimal
    total_ev: Decimal
    total_ac: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    cpi_status: CpiStatus
    cpi_message: str
    spi_status: SpiStatus
    spi_message: str


class ProjectDetail(ProjectRead):
    activities: list[ActivityWithIndicators]
    consolidated: ProjectConsolidatedIndicatorsSchema
