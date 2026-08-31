"""
Métricas Prometheus relacionadas
ao Continuous Profiling.
"""

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)


PROFILING_RUNS = Counter(
    "profiling_runs_total",
    "Quantidade de execuções do profiler.",
    ["service"],
)


PROFILING_DURATION = Histogram(
    "profiling_duration_seconds",
    "Tempo necessário para executar profiling.",
    ["service"],
)


MEMORY_USAGE = Gauge(
    "profiling_memory_bytes",
    "Memória observada pelo profiler.",
    ["service"],
)


HOTSPOT_CPU_PERCENTAGE = Gauge(
    "profiling_hotspot_cpu_percentage",
    "Percentual estimado de concentração no hotspot.",
    ["service"],
)