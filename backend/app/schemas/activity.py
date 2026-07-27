from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.services.evm.enums import CpiStatus, SpiStatus

ACTIVITY_NAME_MAX_LENGTH = 200


class ActivityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=ACTIVITY_NAME_MAX_LENGTH)
    bac: Decimal = Field(gt=0)
    planned_progress: Decimal = Field(ge=0, le=100)
    actual_progress: Decimal = Field(ge=0, le=100)
    ac: Decimal = Field(ge=0)


class ActivityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=ACTIVITY_NAME_MAX_LENGTH)
    bac: Decimal | None = Field(default=None, gt=0)
    planned_progress: Decimal | None = Field(default=None, ge=0, le=100)
    actual_progress: Decimal | None = Field(default=None, ge=0, le=100)
    ac: Decimal | None = Field(default=None, ge=0)


class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    bac: Decimal
    planned_progress: Decimal
    actual_progress: Decimal
    ac: Decimal


class ActivityIndicatorsSchema(BaseModel):
    pv: Decimal
    ev: Decimal
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


class ActivityWithIndicators(ActivityRead):
    indicators: ActivityIndicatorsSchema
