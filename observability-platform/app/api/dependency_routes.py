"""
API do Service Dependency Graph.
"""

from fastapi import (
    APIRouter,
    HTTPException,
)

from pydantic import (
    BaseModel,
)

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

from app.observability.dependency_metrics import (
    BLAST_RADIUS_SCORE,
    BLAST_RADIUS_SIZE,
    DEPENDENCIES_TOTAL,
    SERVICES_TOTAL,
)


router = APIRouter(
    prefix="/api/dependencies",
    tags=[
        "Dependency Intelligence"
    ],
)


graph = DependencyGraph()


class ServiceRequest(
    BaseModel
):

    name: str

    criticality: str = "medium"

    service_type: str = "service"

    healthy: bool = True

    version: str | None = None


class DependencyRequest(
    BaseModel
):

    source: str

    target: str

    dependency_type: str = "runtime"

    critical: bool = False

    weight: float = 1.0


@router.post(
    "/services"
)
def create_service(
    request: ServiceRequest,
):

    service = ServiceNode(
        name=request.name,
        criticality=request.criticality,
        service_type=request.service_type,
        healthy=request.healthy,
        version=request.version,
    )

    graph.add_service(
        service
    )

    SERVICES_TOTAL.set(
        graph.service_count()
    )

    return {
        "status": "created",
        "service": request.name,
    }


@router.post(
    "/relationships"
)
def create_dependency(
    request: DependencyRequest,
):

    if (
        request.source
        not in graph.nodes
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "Source service "
                "not found."
            ),
        )

    if (
        request.target
        not in graph.nodes
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "Target service "
                "not found."
            ),
        )

    dependency = ServiceDependency(
        source=request.source,
        target=request.target,
        dependency_type=(
            request.dependency_type
        ),
        critical=request.critical,
        weight=request.weight,
    )

    graph.add_dependency(
        dependency
    )

    DEPENDENCIES_TOTAL.set(
        graph.dependency_count()
    )

    return {
        "status": "created",
        "source": request.source,
        "target": request.target,
    }


@router.get(
    "/services/{service_name}"
)
def get_service_analysis(
    service_name: str,
):

    result = analyze_service(
        graph,
        service_name,
    )

    if result["status"] == "not_found":

        raise HTTPException(
            status_code=404,
            detail="Service not found.",
        )

    blast_radius = (
        result["blast_radius"]
    )

    BLAST_RADIUS_SIZE.labels(
        service=service_name
    ).set(
        len(blast_radius)
    )

    maximum_score = max(
        [
            item["impact_score"]
            for item in blast_radius
        ],
        default=0,
    )

    BLAST_RADIUS_SCORE.labels(
        service=service_name
    ).set(
        maximum_score
    )

    return result


@router.get(
    "/graph"
)
def get_graph():

    return {
        "services": [
            {
                "name": service.name,
                "criticality": (
                    service.criticality
                ),
                "type": (
                    service.service_type
                ),
                "healthy": service.healthy,
                "version": service.version,
            }
            for service
            in graph.nodes.values()
        ],
        "dependencies": [
            {
                "source": edge.source,
                "target": edge.target,
                "type": (
                    edge.dependency_type
                ),
                "critical": edge.critical,
                "weight": edge.weight,
            }
            for edge
            in graph.edges
        ],
    }