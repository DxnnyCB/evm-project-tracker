from decimal import Decimal

from app.services.evm.enums import CpiStatus, SpiStatus
from app.services.evm.interpreter import interpret_cpi, interpret_spi


def test_interpret_cpi_returns_under_budget_status_when_cpi_greater_than_one() -> None:
    result = interpret_cpi(cpi=Decimal("1.25"), ev=Decimal("6000000"), ac=Decimal("4800000"))

    assert result.status == CpiStatus.UNDER_BUDGET
    assert result.message == (
        "Bajo presupuesto: el proyecto está gastando menos de lo planificado "
        "para el avance logrado."
    )


def test_interpret_cpi_returns_over_budget_status_when_cpi_less_than_one() -> None:
    result = interpret_cpi(cpi=Decimal("0.8"), ev=Decimal("4000000"), ac=Decimal("5000000"))

    assert result.status == CpiStatus.OVER_BUDGET
    assert result.message == (
        "Sobre presupuesto: el proyecto está gastando más de lo planificado para el avance logrado."
    )


def test_interpret_cpi_returns_on_budget_status_when_cpi_equals_one() -> None:
    result = interpret_cpi(cpi=Decimal("1"), ev=Decimal("5000000"), ac=Decimal("5000000"))

    assert result.status == CpiStatus.ON_BUDGET
    assert result.message == "En presupuesto: el gasto coincide con el valor ganado."


def test_interpret_cpi_returns_insufficient_data_status_when_ev_and_ac_are_both_zero() -> None:
    result = interpret_cpi(cpi=None, ev=Decimal("0"), ac=Decimal("0"))

    assert result.status == CpiStatus.INSUFFICIENT_DATA
    assert result.message == "Sin datos suficientes para evaluar el desempeño de costos."


def test_interpret_cpi_returns_cost_not_recorded_status_when_ac_zero_ev_positive() -> None:
    result = interpret_cpi(cpi=None, ev=Decimal("1000000"), ac=Decimal("0"))

    assert result.status == CpiStatus.COST_NOT_RECORDED
    assert result.message == (
        "Hay avance registrado pero aún no se ha cargado el costo real de esta actividad."
    )


def test_interpret_spi_returns_ahead_of_schedule_status_when_spi_greater_than_one() -> None:
    result = interpret_spi(spi=Decimal("1.25"), ev=Decimal("6000000"), pv=Decimal("4800000"))

    assert result.status == SpiStatus.AHEAD_OF_SCHEDULE
    assert result.message == (
        "Adelantado: el avance real supera al avance planificado para esta fecha."
    )


def test_interpret_spi_returns_behind_schedule_status_when_spi_less_than_one() -> None:
    result = interpret_spi(spi=Decimal("0.8"), ev=Decimal("4000000"), pv=Decimal("5000000"))

    assert result.status == SpiStatus.BEHIND_SCHEDULE
    assert result.message == (
        "Atrasado: el avance real está por debajo del avance planificado para esta fecha."
    )


def test_interpret_spi_returns_on_schedule_status_when_spi_equals_one() -> None:
    result = interpret_spi(spi=Decimal("1"), ev=Decimal("5000000"), pv=Decimal("5000000"))

    assert result.status == SpiStatus.ON_SCHEDULE
    assert result.message == "En cronograma: el avance real coincide con el avance planificado."


def test_interpret_spi_returns_insufficient_data_status_when_ev_and_pv_are_both_zero() -> None:
    result = interpret_spi(spi=None, ev=Decimal("0"), pv=Decimal("0"))

    assert result.status == SpiStatus.INSUFFICIENT_DATA
    assert result.message == "Sin datos suficientes para evaluar el cronograma."


def test_interpret_spi_returns_progress_not_recorded_status_when_pv_zero_ev_positive() -> None:
    result = interpret_spi(spi=None, ev=Decimal("1000000"), pv=Decimal("0"))

    assert result.status == SpiStatus.PROGRESS_NOT_RECORDED
    assert result.message == (
        "Hay avance real registrado pero aún no hay avance planificado para esta fecha."
    )
