"""
Blast Radius Engine.

Calcula o impacto potencial da falha
de determinado serviço.
"""

from dataclasses import dataclass

from app.dependency.graph import (
    DependencyGraph,
)


@dataclass
class ImpactedService:
    """
    Representa um serviço potencialmente
    afetado.
    """

    service: str

    distance: int

    criticality: str

    impact_score: float


def calculate_blast_radius(
    graph: DependencyGraph,
    failed_service: str,
) -> list[ImpactedService]:
    """
    Calcula quais serviços podem ser
    afetados pela falha de um serviço.

    Utiliza uma busca em largura (BFS)
    pelo grafo reverso de dependências.
    """

    if failed_service not in graph.nodes:
        return []

    impacted = []

    visited = {
        failed_service
    }

    queue = [
        (
            failed_service,
            0,
        )
    ]

    while queue:

        current, distance = (
            queue.pop(0)
        )

        dependents = (
            graph.get_dependents(
                current
            )
        )

        for dependent in dependents:

            if dependent in visited:
                continue

            visited.add(
                dependent
            )

            node = graph.get_service(
                dependent
            )

            if node is None:
                continue

            impact = calculate_impact_score(
                criticality=node.criticality,
                distance=distance + 1,
            )

            impacted.append(
                ImpactedService(
                    service=dependent,
                    distance=distance + 1,
                    criticality=node.criticality,
                    impact_score=impact,
                )
            )

            queue.append(
                (
                    dependent,
                    distance + 1,
                )
            )

    return sorted(
        impacted,
        key=lambda item:
        item.impact_score,
        reverse=True,
    )


def calculate_impact_score(
    criticality: str,
    distance: int,
) -> float:
    """
    Calcula o impacto potencial.

    Quanto menor a distância até o serviço
    afetado e maior a criticidade,
    maior o impacto.
    """

    criticality_score = {
        "critical": 100,
        "high": 80,
        "medium": 50,
        "low": 20,
    }.get(
        criticality.lower(),
        20,
    )

    distance_factor = max(
        0.1,
        1 / distance,
    )

    return round(
        criticality_score
        * distance_factor,
        2,
    )