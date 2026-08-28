from app.reliability.slo import (
    evaluate_slo,
)


def test_slo_is_met():

    assert evaluate_slo(
        actual_value=99.95,
        target=99.9,
    )


def test_slo_is_not_met():

    assert not evaluate_slo(
        actual_value=99.5,
        target=99.9,
    )