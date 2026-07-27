from decimal import Decimal

PERCENTAGE_DIVISOR = Decimal("100")


def calculate_pv(bac: Decimal, planned_progress: Decimal) -> Decimal:
    """Planned Value: cuánto trabajo debería estar hecho, en dinero, a la fecha de corte."""
    return (planned_progress / PERCENTAGE_DIVISOR) * bac


def calculate_ev(bac: Decimal, actual_progress: Decimal) -> Decimal:
    """Earned Value: cuánto trabajo se ha completado realmente, en dinero."""
    return (actual_progress / PERCENTAGE_DIVISOR) * bac


def calculate_cv(ev: Decimal, ac: Decimal) -> Decimal:
    """Cost Variance: desviación en dinero entre lo ganado y lo gastado. Negativo = sobrecosto."""
    return ev - ac


def calculate_sv(ev: Decimal, pv: Decimal) -> Decimal:
    """Schedule Variance: desviación en trabajo ganado vs. planificado. Negativo = atraso."""
    return ev - pv


def calculate_cpi(ev: Decimal, ac: Decimal) -> Decimal | None:
    """Cost Performance Index: eficiencia de costos. None si AC=0 (no evaluable)."""
    if ac == 0:
        return None
    return ev / ac


def calculate_spi(ev: Decimal, pv: Decimal) -> Decimal | None:
    """Schedule Performance Index: eficiencia de cronograma. None si PV=0 (no evaluable)."""
    if pv == 0:
        return None
    return ev / pv


def calculate_eac(bac: Decimal, cpi: Decimal | None) -> Decimal | None:
    """Estimate at Completion: costo final proyectado. None si CPI no es evaluable."""
    if cpi is None or cpi == 0:
        return None
    return bac / cpi


def calculate_vac(bac: Decimal, eac: Decimal | None) -> Decimal | None:
    """Variance at Completion: desviación proyectada del presupuesto. None si EAC es None."""
    if eac is None:
        return None
    return bac - eac
