from app.intelligence.scoring import (
    calculate_root_cause_score,
)


def test_root_cause_score():

    score = calculate_root_cause_score(
        temporal_correlation=90,
        service_correlation=80,
        severity=70,
        dependency_correlation=90,
        change_correlation=100,
    )

    assert score > 0

    assert score <= 100