from app.reliability.sli import (
    calculate_availability,
    calculate_error_rate,
    calculate_success_rate,
)


def test_availability():

    result = calculate_availability(
        successful_requests=9990,
        total_requests=10000,
    )

    assert result == 99.9


def test_error_rate():

    result = calculate_error_rate(
        failed_requests=100,
        total_requests=10000,
    )

    assert result == 1.0


def test_success_rate():

    result = calculate_success_rate(
        successful_requests=9900,
        total_requests=10000,
    )

    assert result == 99.0