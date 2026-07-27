from decimal import Decimal

from app.services.evm.calculator import calculate_ev, calculate_pv


def test_calculate_pv_returns_planned_progress_times_bac() -> None:
    bac = Decimal("8000000")
    planned_progress = Decimal("60")

    pv = calculate_pv(bac=bac, planned_progress=planned_progress)

    assert pv == Decimal("4800000")


def test_calculate_pv_with_zero_planned_progress_returns_zero() -> None:
    bac = Decimal("8000000")
    planned_progress = Decimal("0")

    pv = calculate_pv(bac=bac, planned_progress=planned_progress)

    assert pv == Decimal("0")


def test_calculate_ev_returns_actual_progress_times_bac() -> None:
    bac = Decimal("8000000")
    actual_progress = Decimal("70")

    ev = calculate_ev(bac=bac, actual_progress=actual_progress)

    assert ev == Decimal("5600000")


def test_calculate_ev_with_zero_actual_progress_returns_zero() -> None:
    bac = Decimal("8000000")
    actual_progress = Decimal("0")

    ev = calculate_ev(bac=bac, actual_progress=actual_progress)

    assert ev == Decimal("0")
