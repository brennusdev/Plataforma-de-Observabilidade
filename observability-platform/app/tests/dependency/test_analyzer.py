from app.dependency.analyzer import (
    analyze_service,
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


def test_service_analysis():

    graph = DependencyGraph()

    graph.add_service(
        ServiceNode(
            name="api",
            criticality="critical",
        )
    )

    graph.add_service(
        ServiceNode(
            name="postgres",
            criticality="critical",
        )
    )

    graph.add_dependency(
        ServiceDependency(
            source="api",
            target="postgres",
        )
    )

    result = analyze_service(
        graph,
        "postgres",
    )

    assert (
        result["status"]
        == "analyzed"
    )

    assert (
        len(
            result["blast_radius"]
        )
        == 1
    )