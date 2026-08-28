"""
Error Budget.

Representa quanto de falha o sistema
pode consumir sem violar o SLO.
"""


def calculate_error_budget(
    slo_target: float,
) -> float:
    """
    Calcula o Error Budget percentual.

    Exemplo:

    SLO = 99.9%

    Error Budget = 0.1%
    """

    return round(
        100 - slo_target,
        4,
    )


def calculate_budget_consumed(
    slo_target: float,
    actual_value: float,
) -> float:
    """
    Calcula quanto do Error Budget
    foi consumido.
    """

    budget = calculate_error_budget(
        slo_target
    )

    if budget <= 0:
        return 0.0

    failure = max(
        0,
        slo_target - actual_value,
    )

    consumed = (
        failure / budget
    ) * 100

    return round(
        min(consumed, 100),
        2,
    )


def calculate_budget_remaining(
    slo_target: float,
    actual_value: float,
) -> float:
    """
    Calcula quanto do Error Budget
    ainda está disponível.
    """

    consumed = calculate_budget_consumed(
        slo_target,
        actual_value,
    )

    return round(
        max(
            0,
            100 - consumed,
        ),
        2,
    )