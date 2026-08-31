from app.profiling.cpu import (
    profile_function,
)


def expensive_function():

    result = 0

    for number in range(
        10_000
    ):

        result += (
            number * number
        )

    return result


def test_profile_function():

    hotspots = profile_function(
        expensive_function
    )

    assert isinstance(
        hotspots,
        list,
    )

    assert len(
        hotspots
    ) > 0