"""
Representação dos nós do Dependency Graph.
"""

from dataclasses import dataclass


@dataclass
class ServiceNode:
    """
    Representa um serviço dentro
    da arquitetura.

    Exemplo:

        api-gateway
        postgres
        redis
        kafka
    """

    name: str

    criticality: str = "medium"

    service_type: str = "service"

    healthy: bool = True

    version: str | None = None