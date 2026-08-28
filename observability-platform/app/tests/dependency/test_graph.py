from app.dependency.edge import (
    ServiceDependency,
)

from app.dependency.graph import (
    DependencyGraph,
)

from app.dependency.node import (
    ServiceNode,
)


def create_graph():

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

    graph.add_service(
        ServiceNode(
            name="redis",
            criticality="high",
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
            source="api",
            target="redis",
        )
    )

    return graph


def test_dependency_graph():

    graph = create_graph()

    assert (
        graph.service_count()
        == 3
    )

    assert (
        graph.dependency_count()
        == 2
    )


def test_get_dependencies():

    graph = create_graph()

    dependencies = (
        graph.get_dependencies(
            "api"
        )
    )

    assert "postgres" in dependencies

    assert "redis" in dependencies