"""
Service Level Objectives.

SLO define o nível de confiabilidade
que queremos atingir.
"""

from dataclasses import dataclass


@dataclass
class SLODefinition:
    """
    Define um SLO.

    Exemplo:

    availability >= 99.9%
    """

    name: str

    service: str

    indicator: str

    target: float

    window_days: int = 30


def evaluate_slo(
    actual_value: float,
    target: float,
) -> bool:
    """
    Verifica se o valor observado
    atingiu o objetivo.
    """

    return actual_value >= target