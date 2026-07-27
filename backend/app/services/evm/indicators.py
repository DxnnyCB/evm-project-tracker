from decimal import Decimal
from typing import NamedTuple

from app.services.evm.calculator import (
    calculate_cpi,
    calculate_cv,
    calculate_eac,
    calculate_ev,
    calculate_pv,
    calculate_spi,
    calculate_sv,
    calculate_vac,
)
from app.services.evm.interpreter import (
    CpiInterpretation,
    SpiInterpretation,
    interpret_cpi,
    interpret_spi,
)


class ActivityInput(NamedTuple):
    bac: Decimal
    planned_progress: Decimal
    actual_progress: Decimal
    ac: Decimal


class ActivityIndicators(NamedTuple):
    pv: Decimal
    ev: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    cpi_interpretation: CpiInterpretation
    spi_interpretation: SpiInterpretation


class ProjectConsolidatedIndicators(NamedTuple):
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
    cpi_interpretation: CpiInterpretation
    spi_interpretation: SpiInterpretation


def calculate_activity_indicators(
    bac: Decimal,
    planned_progress: Decimal,
    actual_progress: Decimal,
    ac: Decimal,
) -> ActivityIndicators:
    """Calcula los 8 indicadores EVM y su interpretación para una sola actividad."""
    pv = calculate_pv(bac, planned_progress)
    ev = calculate_ev(bac, actual_progress)
    cv = calculate_cv(ev, ac)
    sv = calculate_sv(ev, pv)
    cpi = calculate_cpi(ev, ac)
    spi = calculate_spi(ev, pv)
    eac = calculate_eac(bac, cpi)
    vac = calculate_vac(bac, eac)

    return ActivityIndicators(
        pv=pv,
        ev=ev,
        cv=cv,
        sv=sv,
        cpi=cpi,
        spi=spi,
        eac=eac,
        vac=vac,
        cpi_interpretation=interpret_cpi(cpi, ev, ac),
        spi_interpretation=interpret_spi(spi, ev, pv),
    )


def calculate_project_consolidated(
    activities: list[ActivityInput],
) -> ProjectConsolidatedIndicators:
    """Consolida indicadores sumando PV/EV/AC/BAC de todas las actividades primero,
    y derivando CPI/SPI/EAC/VAC solo sobre esos totales — nunca promediando los
    índices individuales de cada actividad."""
    total_bac = sum((activity.bac for activity in activities), start=Decimal("0"))
    total_pv = sum(
        (calculate_pv(activity.bac, activity.planned_progress) for activity in activities),
        start=Decimal("0"),
    )
    total_ev = sum(
        (calculate_ev(activity.bac, activity.actual_progress) for activity in activities),
        start=Decimal("0"),
    )
    total_ac = sum((activity.ac for activity in activities), start=Decimal("0"))

    cv = calculate_cv(total_ev, total_ac)
    sv = calculate_sv(total_ev, total_pv)
    cpi = calculate_cpi(total_ev, total_ac)
    spi = calculate_spi(total_ev, total_pv)
    eac = calculate_eac(total_bac, cpi)
    vac = calculate_vac(total_bac, eac)

    return ProjectConsolidatedIndicators(
        total_bac=total_bac,
        total_pv=total_pv,
        total_ev=total_ev,
        total_ac=total_ac,
        cv=cv,
        sv=sv,
        cpi=cpi,
        spi=spi,
        eac=eac,
        vac=vac,
        cpi_interpretation=interpret_cpi(cpi, total_ev, total_ac),
        spi_interpretation=interpret_spi(spi, total_ev, total_pv),
    )
