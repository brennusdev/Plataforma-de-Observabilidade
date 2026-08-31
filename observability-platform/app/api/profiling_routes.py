"""
API do Continuous Profiling.
"""

import time

from fastapi import (
    APIRouter,
)

from pydantic import (
    BaseModel,
)

from app.observability.profiling_metrics import (
    HOTSPOT_CPU_PERCENTAGE,
    MEMORY_USAGE,
    PROFILING_DURATION,
    PROFILING_RUNS,
)

from app.profiling.analyzer import (
    analyze_snapshot,
)

from app.profiling.profiler import (
    ContinuousProfiler,
)


router = APIRouter(
    prefix="/api/profiling",
    tags=[
        "Continuous Profiling"
    ],
)


profilers: dict[
    str,
    ContinuousProfiler,
] = {}


class ProfilingRequest(
    BaseModel
):

    service: str


def example_workload():

    total = 0

    for number in range(
        100_000
    ):

        total += (
            number
            * number
        )

    return total


@router.post(
    "/run"
)
def run_profiling(
    request: ProfilingRequest,
):

    service = request.service

    if service not in profilers:

        profilers[service] = (
            ContinuousProfiler(
                service_name=service
            )
        )

    profiler = profilers[
        service
    ]

    start = time.perf_counter()

    snapshot = profiler.profile(
        example_workload
    )

    duration = (
        time.perf_counter()
        - start
    )

    PROFILING_RUNS.labels(
        service=service
    ).inc()

    PROFILING_DURATION.labels(
        service=service
    ).observe(
        duration
    )

    MEMORY_USAGE.labels(
        service=service
    ).set(
        snapshot.memory_bytes
    )

    analysis = analyze_snapshot(
        snapshot
    )

    HOTSPOT_CPU_PERCENTAGE.labels(
        service=service
    ).set(
        analysis.get(
            "cpu_percentage",
            0,
        )
    )

    return {
        "snapshot": {
            "service": (
                snapshot.service
            ),
            "timestamp": (
                snapshot.timestamp
            ),
            "cpu_time": (
                snapshot.cpu_time
            ),
            "memory_bytes": (
                snapshot.memory_bytes
            ),
            "hotspots": (
                snapshot.hotspots
            ),
            "memory_changes": (
                snapshot.memory_changes
            ),
        },
        "analysis": analysis,
    }