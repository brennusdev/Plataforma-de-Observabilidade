"""
Representação das relações entre serviços.
"""

from dataclasses import dataclass


@dataclass
class ServiceDependency:
    """
    Representa uma dependência.

    Exemplo:

        api-gateway -> postgres

    significa que api-gateway depende
    de postgres.
    """

    source: str

    target: str

    dependency_type: str = "runtime"

    critical: bool = False

    weight: float = 1.0