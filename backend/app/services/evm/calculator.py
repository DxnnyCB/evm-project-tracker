from decimal import Decimal

PERCENTAGE_DIVISOR = Decimal("100")


def calculate_pv(bac: Decimal, planned_progress: Decimal) -> Decimal:
    """Planned Value: cuánto trabajo debería estar hecho, en dinero, a la fecha de corte."""
    return (planned_progress / PERCENTAGE_DIVISOR) * bac


def calculate_ev(bac: Decimal, actual_progress: Decimal) -> Decimal:
    """Earned Value: cuánto trabajo se ha completado realmente, en dinero."""
    return (actual_progress / PERCENTAGE_DIVISOR) * bac
