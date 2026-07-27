from decimal import ROUND_HALF_UP, Decimal

PRESENTATION_EXPONENT = Decimal("0.01")


def round_for_presentation(value: Decimal) -> Decimal:
    """Redondea a 2 decimales para la respuesta del API.

    Esto es exclusivamente para presentación: `calculator.py` sigue trabajando
    con la precisión completa de `Decimal` (sin redondear divisiones como
    CPI = EV/AC), para no acumular error en cálculos derivados como
    EAC = BAC/CPI. El redondeo ocurre solo aquí, al construir el JSON final.
    """
    return value.quantize(PRESENTATION_EXPONENT, rounding=ROUND_HALF_UP)


def round_for_presentation_optional(value: Decimal | None) -> Decimal | None:
    """Igual que `round_for_presentation`, pero preserva `None` (índices indeterminados)."""
    return None if value is None else round_for_presentation(value)
