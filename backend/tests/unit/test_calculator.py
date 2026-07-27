from decimal import Decimal

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


def test_calculate_cv_returns_positive_when_ev_greater_than_ac() -> None:
    ev = Decimal("5600000")
    ac = Decimal("5000000")

    cv = calculate_cv(ev=ev, ac=ac)

    assert cv == Decimal("600000")


def test_calculate_cv_returns_negative_when_ev_less_than_ac() -> None:
    ev = Decimal("5600000")
    ac = Decimal("6000000")

    cv = calculate_cv(ev=ev, ac=ac)

    assert cv == Decimal("-400000")


def test_calculate_cv_returns_zero_when_ev_equals_ac() -> None:
    ev = Decimal("5600000")
    ac = Decimal("5600000")

    cv = calculate_cv(ev=ev, ac=ac)

    assert cv == Decimal("0")


def test_calculate_sv_returns_positive_when_ev_greater_than_pv() -> None:
    ev = Decimal("5600000")
    pv = Decimal("4800000")

    sv = calculate_sv(ev=ev, pv=pv)

    assert sv == Decimal("800000")


def test_calculate_sv_returns_negative_when_ev_less_than_pv() -> None:
    ev = Decimal("4000000")
    pv = Decimal("4800000")

    sv = calculate_sv(ev=ev, pv=pv)

    assert sv == Decimal("-800000")


def test_calculate_sv_returns_zero_when_ev_equals_pv() -> None:
    ev = Decimal("4800000")
    pv = Decimal("4800000")

    sv = calculate_sv(ev=ev, pv=pv)

    assert sv == Decimal("0")


def test_calculate_cpi_returns_ev_divided_by_ac() -> None:
    ev = Decimal("5600000")
    ac = Decimal("5000000")

    cpi = calculate_cpi(ev=ev, ac=ac)

    assert cpi == Decimal("1.12")


def test_calculate_cpi_returns_none_when_ev_and_ac_are_both_zero() -> None:
    ev = Decimal("0")
    ac = Decimal("0")

    cpi = calculate_cpi(ev=ev, ac=ac)

    assert cpi is None


def test_calculate_cpi_returns_none_when_ac_is_zero_and_ev_is_positive() -> None:
    ev = Decimal("1000000")
    ac = Decimal("0")

    cpi = calculate_cpi(ev=ev, ac=ac)

    assert cpi is None


def test_calculate_spi_returns_ev_divided_by_pv() -> None:
    ev = Decimal("6000000")
    pv = Decimal("4800000")

    spi = calculate_spi(ev=ev, pv=pv)

    assert spi == Decimal("1.25")


def test_calculate_spi_returns_none_when_ev_and_pv_are_both_zero() -> None:
    ev = Decimal("0")
    pv = Decimal("0")

    spi = calculate_spi(ev=ev, pv=pv)

    assert spi is None


def test_calculate_spi_returns_none_when_pv_is_zero_and_ev_is_positive() -> None:
    ev = Decimal("1000000")
    pv = Decimal("0")

    spi = calculate_spi(ev=ev, pv=pv)

    assert spi is None


def test_calculate_eac_returns_bac_divided_by_cpi() -> None:
    bac = Decimal("8000000")
    cpi = Decimal("1.25")

    eac = calculate_eac(bac=bac, cpi=cpi)

    assert eac == Decimal("6400000")


def test_calculate_eac_returns_none_when_cpi_is_none() -> None:
    bac = Decimal("8000000")

    eac = calculate_eac(bac=bac, cpi=None)

    assert eac is None


def test_calculate_eac_returns_none_when_cpi_is_zero() -> None:
    bac = Decimal("8000000")
    cpi = Decimal("0")

    eac = calculate_eac(bac=bac, cpi=cpi)

    assert eac is None


def test_calculate_vac_returns_bac_minus_eac() -> None:
    bac = Decimal("8000000")
    eac = Decimal("6400000")

    vac = calculate_vac(bac=bac, eac=eac)

    assert vac == Decimal("1600000")


def test_calculate_vac_returns_none_when_eac_is_none() -> None:
    bac = Decimal("8000000")

    vac = calculate_vac(bac=bac, eac=None)

    assert vac is None
