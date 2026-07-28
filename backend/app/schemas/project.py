from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.activity import ActivityWithIndicators
from app.schemas.rounding import round_for_presentation, round_for_presentation_optional
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
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_bac": "8000000.00",
                "total_pv": "8000000.00",
                "total_ev": "5600000.00",
                "total_ac": "6000000.00",
                "cv": "-400000.00",
                "sv": "-2400000.00",
                "cpi": "0.93",
                "spi": "0.70",
                "eac": "8571428.57",
                "vac": "-571428.57",
                "cpi_status": "over_budget",
                "cpi_message": (
                    "Sobre presupuesto: el proyecto está gastando más de lo "
                    "planificado para el avance logrado."
                ),
                "spi_status": "behind_schedule",
                "spi_message": (
                    "Atrasado: el avance real está por debajo del avance "
                    "planificado para esta fecha."
                ),
            }
        }
    )

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
            total_bac=round_for_presentation(consolidated.total_bac),
            total_pv=round_for_presentation(consolidated.total_pv),
            total_ev=round_for_presentation(consolidated.total_ev),
            total_ac=round_for_presentation(consolidated.total_ac),
            cv=round_for_presentation(consolidated.cv),
            sv=round_for_presentation(consolidated.sv),
            cpi=round_for_presentation_optional(consolidated.cpi),
            spi=round_for_presentation_optional(consolidated.spi),
            eac=round_for_presentation_optional(consolidated.eac),
            vac=round_for_presentation_optional(consolidated.vac),
            cpi_status=consolidated.cpi_interpretation.status,
            cpi_message=consolidated.cpi_interpretation.message,
            spi_status=consolidated.spi_interpretation.status,
            spi_message=consolidated.spi_interpretation.message,
        )


class ProjectDetail(ProjectRead):
    activities: list[ActivityWithIndicators]
    consolidated: ProjectConsolidatedIndicatorsSchema
