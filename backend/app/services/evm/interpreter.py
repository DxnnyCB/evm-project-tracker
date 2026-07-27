from decimal import Decimal
from typing import NamedTuple

from app.services.evm.enums import CpiStatus, SpiStatus

_MSG_CPI_UNDER_BUDGET = (
    "Bajo presupuesto: el proyecto está gastando menos de lo planificado para el avance logrado."
)
_MSG_CPI_OVER_BUDGET = (
    "Sobre presupuesto: el proyecto está gastando más de lo planificado para el avance logrado."
)
_MSG_CPI_ON_BUDGET = "En presupuesto: el gasto coincide con el valor ganado."
_MSG_CPI_INSUFFICIENT_DATA = "Sin datos suficientes para evaluar el desempeño de costos."
_MSG_CPI_COST_NOT_RECORDED = (
    "Hay avance registrado pero aún no se ha cargado el costo real de esta actividad."
)

_MSG_SPI_AHEAD_OF_SCHEDULE = (
    "Adelantado: el avance real supera al avance planificado para esta fecha."
)
_MSG_SPI_BEHIND_SCHEDULE = (
    "Atrasado: el avance real está por debajo del avance planificado para esta fecha."
)
_MSG_SPI_ON_SCHEDULE = "En cronograma: el avance real coincide con el avance planificado."
_MSG_SPI_INSUFFICIENT_DATA = "Sin datos suficientes para evaluar el cronograma."
_MSG_SPI_PROGRESS_NOT_RECORDED = (
    "Hay avance real registrado pero aún no hay avance planificado para esta fecha."
)


class CpiInterpretation(NamedTuple):
    status: CpiStatus
    message: str


class SpiInterpretation(NamedTuple):
    status: SpiStatus
    message: str


def interpret_cpi(cpi: Decimal | None, ev: Decimal, ac: Decimal) -> CpiInterpretation:
    """Interpreta el CPI. Cuando es None, usa ev/ac para distinguir la causa."""
    if cpi is None:
        if ac == 0 and ev == 0:
            return CpiInterpretation(CpiStatus.INSUFFICIENT_DATA, _MSG_CPI_INSUFFICIENT_DATA)
        return CpiInterpretation(CpiStatus.COST_NOT_RECORDED, _MSG_CPI_COST_NOT_RECORDED)

    if cpi > 1:
        return CpiInterpretation(CpiStatus.UNDER_BUDGET, _MSG_CPI_UNDER_BUDGET)
    if cpi < 1:
        return CpiInterpretation(CpiStatus.OVER_BUDGET, _MSG_CPI_OVER_BUDGET)
    return CpiInterpretation(CpiStatus.ON_BUDGET, _MSG_CPI_ON_BUDGET)


def interpret_spi(spi: Decimal | None, ev: Decimal, pv: Decimal) -> SpiInterpretation:
    """Interpreta el SPI. Cuando es None, usa ev/pv para distinguir la causa."""
    if spi is None:
        if pv == 0 and ev == 0:
            return SpiInterpretation(SpiStatus.INSUFFICIENT_DATA, _MSG_SPI_INSUFFICIENT_DATA)
        return SpiInterpretation(SpiStatus.PROGRESS_NOT_RECORDED, _MSG_SPI_PROGRESS_NOT_RECORDED)

    if spi > 1:
        return SpiInterpretation(SpiStatus.AHEAD_OF_SCHEDULE, _MSG_SPI_AHEAD_OF_SCHEDULE)
    if spi < 1:
        return SpiInterpretation(SpiStatus.BEHIND_SCHEDULE, _MSG_SPI_BEHIND_SCHEDULE)
    return SpiInterpretation(SpiStatus.ON_SCHEDULE, _MSG_SPI_ON_SCHEDULE)
