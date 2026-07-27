from decimal import Decimal

from app.services.evm.enums import CpiStatus, SpiStatus
from app.services.evm.indicators import (
    ActivityInput,
    calculate_activity_indicators,
    calculate_project_consolidated,
)


def test_calculate_activity_indicators_returns_all_eight_metrics_with_interpretation() -> None:
    indicators = calculate_activity_indicators(
        bac=Decimal("8000000"),
        planned_progress=Decimal("60"),
        actual_progress=Decimal("70"),
        ac=Decimal("6000000"),
    )

    assert indicators.pv == Decimal("4800000")
    assert indicators.ev == Decimal("5600000")
    assert indicators.cv == Decimal("-400000")
    assert indicators.sv == Decimal("800000")
    assert indicators.cpi.quantize(Decimal("0.0001")) == Decimal("0.9333")
    assert indicators.spi.quantize(Decimal("0.0001")) == Decimal("1.1667")
    assert indicators.eac.quantize(Decimal("0.01")) == Decimal("8571428.57")
    assert indicators.vac.quantize(Decimal("0.01")) == Decimal("-571428.57")
    assert indicators.cpi_interpretation.status == CpiStatus.OVER_BUDGET
    assert indicators.spi_interpretation.status == SpiStatus.AHEAD_OF_SCHEDULE


def test_calculate_activity_indicators_with_zero_actual_progress() -> None:
    indicators = calculate_activity_indicators(
        bac=Decimal("8000000"),
        planned_progress=Decimal("60"),
        actual_progress=Decimal("0"),
        ac=Decimal("1000000"),
    )

    assert indicators.ev == Decimal("0")
    assert indicators.cv == Decimal("-1000000")
    assert indicators.sv == Decimal("-4800000")
    assert indicators.cpi == Decimal("0")
    assert indicators.spi == Decimal("0")
    assert indicators.cpi_interpretation.status == CpiStatus.OVER_BUDGET
    assert indicators.spi_interpretation.status == SpiStatus.BEHIND_SCHEDULE


def test_calculate_activity_indicators_with_ac_zero_and_no_progress_yet() -> None:
    indicators = calculate_activity_indicators(
        bac=Decimal("8000000"),
        planned_progress=Decimal("0"),
        actual_progress=Decimal("0"),
        ac=Decimal("0"),
    )

    assert indicators.pv == Decimal("0")
    assert indicators.ev == Decimal("0")
    assert indicators.cv == Decimal("0")
    assert indicators.sv == Decimal("0")
    assert indicators.cpi is None
    assert indicators.spi is None
    assert indicators.eac is None
    assert indicators.vac is None
    assert indicators.cpi_interpretation.status == CpiStatus.INSUFFICIENT_DATA
    assert indicators.spi_interpretation.status == SpiStatus.INSUFFICIENT_DATA


def test_calculate_project_consolidated_sums_pv_ev_ac_before_deriving_indices() -> None:
    activities = [
        ActivityInput(
            bac=Decimal("3000000"),
            planned_progress=Decimal("80"),
            actual_progress=Decimal("60"),
            ac=Decimal("2000000"),
        ),
        ActivityInput(
            bac=Decimal("3000000"),
            planned_progress=Decimal("50"),
            actual_progress=Decimal("50"),
            ac=Decimal("1500000"),
        ),
        ActivityInput(
            bac=Decimal("2000000"),
            planned_progress=Decimal("40"),
            actual_progress=Decimal("70"),
            ac=Decimal("1600000"),
        ),
    ]

    consolidated = calculate_project_consolidated(activities)

    assert consolidated.total_bac == Decimal("8000000")
    assert consolidated.total_pv == Decimal("4700000")
    assert consolidated.total_ev == Decimal("4700000")
    assert consolidated.total_ac == Decimal("5100000")
    assert consolidated.cv == Decimal("-400000")
    assert consolidated.sv == Decimal("0")
    assert consolidated.cpi.quantize(Decimal("0.0001")) == Decimal("0.9216")
    assert consolidated.spi == Decimal("1")
    assert consolidated.eac.quantize(Decimal("0.01")) == Decimal("8680851.06")
    assert consolidated.vac.quantize(Decimal("0.01")) == Decimal("-680851.06")
    assert consolidated.cpi_interpretation.status == CpiStatus.OVER_BUDGET
    assert consolidated.spi_interpretation.status == SpiStatus.ON_SCHEDULE


def test_calculate_project_consolidated_with_no_activities_returns_none_indicators() -> None:
    consolidated = calculate_project_consolidated([])

    assert consolidated.total_bac == Decimal("0")
    assert consolidated.total_pv == Decimal("0")
    assert consolidated.total_ev == Decimal("0")
    assert consolidated.total_ac == Decimal("0")
    assert consolidated.cv == Decimal("0")
    assert consolidated.sv == Decimal("0")
    assert consolidated.cpi is None
    assert consolidated.spi is None
    assert consolidated.eac is None
    assert consolidated.vac is None
    assert consolidated.cpi_interpretation.status == CpiStatus.INSUFFICIENT_DATA
    assert consolidated.spi_interpretation.status == SpiStatus.INSUFFICIENT_DATA


def test_calculate_project_consolidated_with_single_activity_matches_its_own_indicators() -> None:
    bac = Decimal("8000000")
    planned_progress = Decimal("60")
    actual_progress = Decimal("70")
    ac = Decimal("6000000")

    activity_indicators = calculate_activity_indicators(
        bac=bac, planned_progress=planned_progress, actual_progress=actual_progress, ac=ac
    )
    consolidated = calculate_project_consolidated(
        [
            ActivityInput(
                bac=bac, planned_progress=planned_progress, actual_progress=actual_progress, ac=ac
            )
        ]
    )

    assert consolidated.total_bac == bac
    assert consolidated.total_pv == activity_indicators.pv
    assert consolidated.total_ev == activity_indicators.ev
    assert consolidated.total_ac == ac
    assert consolidated.cv == activity_indicators.cv
    assert consolidated.sv == activity_indicators.sv
    assert consolidated.cpi == activity_indicators.cpi
    assert consolidated.spi == activity_indicators.spi
    assert consolidated.eac == activity_indicators.eac
    assert consolidated.vac == activity_indicators.vac
    assert consolidated.cpi_interpretation == activity_indicators.cpi_interpretation
    assert consolidated.spi_interpretation == activity_indicators.spi_interpretation


def test_calculate_project_consolidated_with_mixed_ac_zero_activities() -> None:
    """Una actividad con AC=0 (CPI individual sería None) no debe romper ni sesgar
    el consolidado: el total de AC del proyecto es > 0, así que el CPI consolidado
    debe ser calculable, derivado de las sumas totales, nunca de índices individuales."""
    activities = [
        ActivityInput(
            bac=Decimal("1000000"),
            planned_progress=Decimal("50"),
            actual_progress=Decimal("50"),
            ac=Decimal("0"),
        ),
        ActivityInput(
            bac=Decimal("1000000"),
            planned_progress=Decimal("50"),
            actual_progress=Decimal("50"),
            ac=Decimal("1000000"),
        ),
    ]

    consolidated = calculate_project_consolidated(activities)

    assert consolidated.total_ac == Decimal("1000000")
    assert consolidated.cpi == Decimal("1")
    assert consolidated.spi == Decimal("1")
    assert consolidated.cpi_interpretation.status == CpiStatus.ON_BUDGET
    assert consolidated.spi_interpretation.status == SpiStatus.ON_SCHEDULE
