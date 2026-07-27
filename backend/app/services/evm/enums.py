from enum import StrEnum


class CpiStatus(StrEnum):
    """Estado de eficiencia de costos, para que el frontend decida el color del semáforo."""

    UNDER_BUDGET = "under_budget"
    OVER_BUDGET = "over_budget"
    ON_BUDGET = "on_budget"
    INSUFFICIENT_DATA = "insufficient_data"
    COST_NOT_RECORDED = "cost_not_recorded"


class SpiStatus(StrEnum):
    """Estado de eficiencia de cronograma, para que el frontend decida el color del semáforo."""

    AHEAD_OF_SCHEDULE = "ahead_of_schedule"
    BEHIND_SCHEDULE = "behind_schedule"
    ON_SCHEDULE = "on_schedule"
    INSUFFICIENT_DATA = "insufficient_data"
    PROGRESS_NOT_RECORDED = "progress_not_recorded"
