from app.dependency.blast_radius import (
    calculate_blast_radius,
)

from app.dependency.edge import (
    ServiceDependency,
)

from app.dependency.graph import (
    DependencyGraph,
)

from app.dependency.node import (
    ServiceNode,
)


def test_blast_radius():

    graph = DependencyGraph()

    graph.add_service(
        ServiceNode(
            name="postgres",
            criticality="critical",
        )
    )

    graph.add_service(
        ServiceNode(
            name="api",
            criticality="high",
        )
    )

    graph.add_service(
        ServiceNode(
            name="frontend",
            criticality="critical",
        )
    )

    graph.add_dependency(
        ServiceDependency(
            source="api",
            target="postgres",
        )
    )

    graph.add_dependency(
        ServiceDependency(
            source="frontend",
            target="api",
        )
    )

    result = calculate_blast_radius(
        graph,
        "postgres",
    )

    services = [
        item.service
        for item in result
    ]

    assert "api" in services

    assert "frontend" in services