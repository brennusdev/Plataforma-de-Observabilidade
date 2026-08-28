"""
Dependency Analyzer.

Produz informações de alto nível
sobre a arquitetura.
"""

from app.dependency.blast_radius import (
    calculate_blast_radius,
)

from app.dependency.graph import (
    DependencyGraph,
)


def analyze_service(
    graph: DependencyGraph,
    service_name: str,
) -> dict:
    """
    Analisa um serviço específico.
    """

    service = graph.get_service(
        service_name
    )

    if service is None:

        return {
            "status": "not_found",
            "service": service_name,
        }

    dependencies = (
        graph.get_dependencies(
            service_name
        )
    )

    dependents = (
        graph.get_dependents(
            service_name
        )
    )

    blast_radius = (
        calculate_blast_radius(
            graph,
            service_name,
        )
    )

    return {
        "status": "analyzed",
        "service": service_name,
        "criticality": (
            service.criticality
        ),
        "healthy": service.healthy,
        "dependencies": dependencies,
        "dependents": dependents,
        "blast_radius": [
            {
                "service": item.service,
                "distance": item.distance,
                "criticality": (
                    item.criticality
                ),
                "impact_score": (
                    item.impact_score
                ),
            }
            for item in blast_radius
        ],
    }