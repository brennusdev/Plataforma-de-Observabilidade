"""
Service Dependency Graph.

Mantém os serviços e as relações
entre eles.
"""

from app.dependency.edge import (
    ServiceDependency,
)

from app.dependency.node import (
    ServiceNode,
)


class DependencyGraph:
    """
    Grafo direcionado de dependências.

    Exemplo:

        frontend
            ↓
        api-gateway
          ↓     ↓
       redis   postgres
                 ↓
               kafka
    """

    def __init__(self):

        self.nodes: dict[
            str,
            ServiceNode,
        ] = {}

        self.edges: list[
            ServiceDependency
        ] = []

    def add_service(
        self,
        service: ServiceNode,
    ) -> None:
        """
        Adiciona um serviço ao grafo.
        """

        self.nodes[
            service.name
        ] = service

    def add_dependency(
        self,
        dependency: ServiceDependency,
    ) -> None:
        """
        Adiciona uma dependência.
        """

        self.edges.append(
            dependency
        )

    def get_dependencies(
        self,
        service_name: str,
    ) -> list[str]:
        """
        Retorna os serviços dos quais
        determinado serviço depende.
        """

        return [
            edge.target
            for edge in self.edges
            if edge.source
            == service_name
        ]

    def get_dependents(
        self,
        service_name: str,
    ) -> list[str]:
        """
        Retorna quais serviços dependem
        de determinado serviço.
        """

        return [
            edge.source
            for edge in self.edges
            if edge.target
            == service_name
        ]

    def get_service(
        self,
        service_name: str,
    ) -> ServiceNode | None:
        """
        Retorna um serviço pelo nome.
        """

        return self.nodes.get(
            service_name
        )

    def service_count(self) -> int:
        """
        Quantidade de serviços.
        """

        return len(
            self.nodes
        )

    def dependency_count(self) -> int:
        """
        Quantidade de relações.
        """

        return len(
            self.edges
        )