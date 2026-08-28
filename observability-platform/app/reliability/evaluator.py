"""
Reliability Evaluator.

Responsável por transformar SLI + SLO
em uma avaliação operacional.
"""

from app.reliability.error_budget import (
    calculate_budget_consumed,
    calculate_budget_remaining,
)

from app.reliability.slo import (
    evaluate_slo,
)


def evaluate_reliability(
    actual_value: float,
    slo_target: float,
) -> dict:
    """
    Avalia a confiabilidade de um serviço.
    """

    slo_met = evaluate_slo(
        actual_value,
        slo_target,
    )

    consumed = (
        calculate_budget_consumed(
            slo_target,
            actual_value,
        )
    )

    remaining = (
        calculate_budget_remaining(
            slo_target,
            actual_value,
        )
    )

    if not slo_met:

        status = "breached"

    elif remaining <= 20:

        status = "critical"

    elif remaining <= 50:

        status = "warning"

    else:

        status = "healthy"

    return {
        "slo_target": slo_target,
        "actual_value": actual_value,
        "slo_met": slo_met,
        "budget_consumed": consumed,
        "budget_remaining": remaining,
        "status": status,
    }