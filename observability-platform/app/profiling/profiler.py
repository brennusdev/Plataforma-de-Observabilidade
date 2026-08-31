"""
Continuous Profiler.

Orquestra CPU e memória.
"""

from datetime import datetime
from typing import Callable

from app.profiling.cpu import (
    profile_function,
)

from app.profiling.memory import (
    start_memory_profiling,
    take_memory_snapshot,
)

from app.profiling.snapshot import (
    ProfilingSnapshot,
)


class ContinuousProfiler:
    """
    Gerenciador de profiling.

    Mantém o estado necessário para comparar
    diferentes momentos da aplicação.
    """

    def __init__(
        self,
        service_name: str,
    ):

        self.service_name = (
            service_name
        )

        self.previous_memory_snapshot = (
            None
        )

    def profile(
        self,
        function: Callable,
        *args,
        **kwargs,
    ) -> ProfilingSnapshot:
        """
        Executa profiling completo.
        """

        start_memory_profiling()

        memory_before = (
            take_memory_snapshot()
        )

        hotspots = profile_function(
            function,
            *args,
            **kwargs,
        )

        memory_after = (
            take_memory_snapshot()
        )

        memory_changes = []

        if (
            self.previous_memory_snapshot
            is not None
        ):

            differences = (
                memory_after.compare_to(
                    self.previous_memory_snapshot,
                    "lineno",
                )
            )

            memory_changes = [
                {
                    "file": str(
                        item.traceback
                    ),
                    "size_diff": (
                        item.size_diff
                    ),
                    "count_diff": (
                        item.count_diff
                    ),
                }
                for item
                in differences[:10]
            ]

        self.previous_memory_snapshot = (
            memory_after
        )

        return ProfilingSnapshot(
            service=self.service_name,
            timestamp=datetime.utcnow(),
            cpu_time=(
                hotspots[0]["cumulative_time"]
                if hotspots
                else 0
            ),
            memory_bytes=(
                sum(
                    stat.size
                    for stat
                    in memory_after.statistics(
                        "lineno"
                    )
                )
            ),
            hotspots=hotspots[:10],
            memory_changes=memory_changes,
        )