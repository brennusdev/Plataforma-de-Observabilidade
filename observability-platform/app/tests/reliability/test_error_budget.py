from app.reliability.error_budget import (
    calculate_error_budget,
    calculate_budget_consumed,
    calculate_budget_remaining,
)


def test_error_budget():

    budget = calculate_error_budget(
        99.9
    )

    assert budget == 0.1


def test_budget_consumption():

    consumed = calculate_budget_consumed(
        slo_target=99.9,
        actual_value=99.8,
    )

    assert consumed == 100


def test_budget_remaining():

    remaining = calculate_budget_remaining(
        slo_target=99.9,
        actual_value=99.9,
    )

    assert remaining == 100