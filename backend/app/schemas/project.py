from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.activity import ActivityWithIndicators
from app.services.evm.enums import CpiStatus, SpiStatus
from app.services.evm.indicators import ProjectConsolidatedIndicators

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

    @classmethod
    def from_domain(cls, consolidated: ProjectConsolidatedIndicators) -> Self:
        """Aplana el `ProjectConsolidatedIndicators` del service al contrato
        plano del API."""
        return cls(
            total_bac=consolidated.total_bac,
            total_pv=consolidated.total_pv,
            total_ev=consolidated.total_ev,
            total_ac=consolidated.total_ac,
            cv=consolidated.cv,
            sv=consolidated.sv,
            cpi=consolidated.cpi,
            spi=consolidated.spi,
            eac=consolidated.eac,
            vac=consolidated.vac,
            cpi_status=consolidated.cpi_interpretation.status,
            cpi_message=consolidated.cpi_interpretation.message,
            spi_status=consolidated.spi_interpretation.status,
            spi_message=consolidated.spi_interpretation.message,
        )


class ProjectDetail(ProjectRead):
    activities: list[ActivityWithIndicators]
    consolidated: ProjectConsolidatedIndicatorsSchema
