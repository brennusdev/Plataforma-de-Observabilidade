from app.profiling.profiler import (
    ContinuousProfiler,
)


def workload():

    result = 0

    for number in range(
        1_000
    ):

        result += number

    return result


def test_continuous_profiler():

    profiler = ContinuousProfiler(
        service_name="test-service"
    )

    snapshot = profiler.profile(
        workload
    )

    assert (
        snapshot.service
        == "test-service"
    )

    assert (
        snapshot.memory_bytes
        >= 0
    )

    assert isinstance(
        snapshot.hotspots,
        list,
    )