from datetime import datetime

from app.profiling.analyzer import (
    analyze_snapshot,
)

from app.profiling.snapshot import (
    ProfilingSnapshot,
)


def test_analyzer():

    snapshot = ProfilingSnapshot(
        service="api",
        timestamp=datetime.utcnow(),
        cpu_time=10.0,
        memory_bytes=1024,
        hotspots=[
            {
                "filename": "app.py",
                "line": 10,
                "function": "slow_function",
                "primitive_calls": 1,
                "total_calls": 1,
                "total_time": 8.0,
                "cumulative_time": 8.0,
            },
            {
                "filename": "app.py",
                "line": 20,
                "function": "other_function",
                "primitive_calls": 1,
                "total_calls": 1,
                "total_time": 2.0,
                "cumulative_time": 2.0,
            },
        ],
        memory_changes=[],
    )

    result = analyze_snapshot(
        snapshot
    )

    assert (
        result["status"]
        == "analyzed"
    )

    assert (
        result["severity"]
        == "high"
    )