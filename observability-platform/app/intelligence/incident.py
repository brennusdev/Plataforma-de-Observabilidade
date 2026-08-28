"""
Estruturas utilizadas pelo Incident Intelligence Engine.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class IncidentSignal:
    """
    Representa um sinal observado durante
    um incidente.

    Exemplos:

    - aumento de erros;
    - aumento de latência;
    - queda de disponibilidade;
    - deployment recente;
    - falha de banco;
    - alteração de infraestrutura.
    """

    source: str

    service: str

    signal_type: str

    value: float

    timestamp: datetime

    severity: str = "warning"

    metadata: dict = field(
        default_factory=dict
    )


@dataclass
class Incident:
    """
    Representa um incidente correlacionado.
    """

    id: str

    title: str

    service: str

    started_at: datetime

    severity: str

    signals: list[
        IncidentSignal
    ] = field(
        default_factory=list
    )