from app.chaos.analyzer import (
    calculate_blast_radius,
    calculate_impact_score,
    calculate_resilience_score,
)


def test_impact_score():

    score = calculate_impact_score(
        error_rate=10,
        latency_increase=20,
        availability_loss=5,
    )

    assert score >= 0

    assert score <= 100


def test_blast_radius():

    radius = calculate_blast_radius(
        affected_services=2,
        total_services=10,
    )

    assert radius == 20


def test_resilience_score():

    score = calculate_resilience_score(
        recovery_time=5,
        impact_score=10,
        availability=99,
    )

    assert score >= 0

    assert score <= 100