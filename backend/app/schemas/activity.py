from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from app.services.evm.enums import CpiStatus, SpiStatus
from app.services.evm.indicators import ActivityIndicators

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

    @classmethod
    def from_domain(cls, indicators: ActivityIndicators) -> Self:
        """Aplana el `ActivityIndicators` del service (con `cpi_interpretation`/
        `spi_interpretation` anidados) al contrato plano del API."""
        return cls(
            pv=indicators.pv,
            ev=indicators.ev,
            cv=indicators.cv,
            sv=indicators.sv,
            cpi=indicators.cpi,
            spi=indicators.spi,
            eac=indicators.eac,
            vac=indicators.vac,
            cpi_status=indicators.cpi_interpretation.status,
            cpi_message=indicators.cpi_interpretation.message,
            spi_status=indicators.spi_interpretation.status,
            spi_message=indicators.spi_interpretation.message,
        )


class ActivityWithIndicators(ActivityRead):
    indicators: ActivityIndicatorsSchema
