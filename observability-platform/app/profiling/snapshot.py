"""
Modelo de snapshot de profiling.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProfilingSnapshot:
    """
    Representa um ponto de observação
    do comportamento da aplicação.
    """

    service: str

    timestamp: datetime

    cpu_time: float

    memory_bytes: int

    hotspots: list[dict]

    memory_changes: list[dict]