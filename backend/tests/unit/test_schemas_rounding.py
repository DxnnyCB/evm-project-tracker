from decimal import Decimal

from app.schemas.activity import ActivityIndicatorsSchema
from app.schemas.project import ProjectConsolidatedIndicatorsSchema
from app.services.evm.indicators import (
    ActivityInput,
    calculate_activity_indicators,
    calculate_project_consolidated,
)


def test_activity_indicators_schema_rounds_non_exact_division_to_two_decimals() -> None:
    """Reproduce el bug reportado: EV/AC no exacto (0.8333...) no debe llegar
    al JSON con 28 decimales."""
    indicators = calculate_activity_indicators(
        bac=Decimal("6000"),
        planned_progress=Decimal("50"),
        actual_progress=Decimal("50"),
        ac=Decimal("3600"),
    )
    assert str(indicators.cpi).startswith("0.833333333333")  # precisión completa en el service

    schema = ActivityIndicatorsSchema.from_domain(indicators)

    assert schema.cpi == Decimal("0.83")
    assert schema.spi == Decimal("1.00")


def test_activity_indicators_schema_preserves_none_for_indeterminate_indices() -> None:
    indicators = calculate_activity_indicators(
        bac=Decimal("6000"),
        planned_progress=Decimal("0"),
        actual_progress=Decimal("0"),
        ac=Decimal("0"),
    )

    schema = ActivityIndicatorsSchema.from_domain(indicators)

    assert schema.cpi is None
    assert schema.spi is None
    assert schema.eac is None
    assert schema.vac is None


def test_project_consolidated_indicators_schema_rounds_non_exact_division_to_two_decimals() -> None:
    consolidated = calculate_project_consolidated(
        [
            ActivityInput(
                bac=Decimal("6000"),
                planned_progress=Decimal("50"),
                actual_progress=Decimal("50"),
                ac=Decimal("3600"),
            )
        ]
    )
    assert str(consolidated.cpi).startswith("0.833333333333")

    schema = ProjectConsolidatedIndicatorsSchema.from_domain(consolidated)

    assert schema.cpi == Decimal("0.83")


def test_project_consolidated_indicators_schema_preserves_none_when_no_activities() -> None:
    consolidated = calculate_project_consolidated([])

    schema = ProjectConsolidatedIndicatorsSchema.from_domain(consolidated)

    assert schema.cpi is None
    assert schema.spi is None
    assert schema.eac is None
    assert schema.vac is None
