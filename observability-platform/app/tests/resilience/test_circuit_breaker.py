from app.core.resilience import (
    CircuitBreaker,
)


def test_circuit_starts_closed():

    breaker = CircuitBreaker()

    assert (
        breaker.state
        == breaker.CLOSED
    )


def test_circuit_opens_after_failures():

    breaker = CircuitBreaker(
        failure_threshold=3
    )

    breaker.record_failure()

    breaker.record_failure()

    breaker.record_failure()

    assert (
        breaker.state
        == breaker.OPEN
    )


def test_success_resets_circuit():

    breaker = CircuitBreaker()

    breaker.record_failure()

    breaker.record_success()

    assert (
        breaker.state
        == breaker.CLOSED
    )

    assert (
        breaker.failure_count
        == 0
    )