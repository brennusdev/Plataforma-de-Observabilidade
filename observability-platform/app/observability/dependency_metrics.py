"""
Métricas Prometheus do Dependency Graph.
"""

from prometheus_client import (
    Gauge,
)


SERVICES_TOTAL = Gauge(
    "dependency_services_total",
    "Quantidade de serviços conhecidos.",
)


DEPENDENCIES_TOTAL = Gauge(
    "dependency_relationships_total",
    "Quantidade de dependências conhecidas.",
)


BLAST_RADIUS_SIZE = Gauge(
    "dependency_blast_radius_size",
    "Quantidade de serviços afetados.",
    ["service"],
)


BLAST_RADIUS_SCORE = Gauge(
    "dependency_blast_radius_score",
    "Score máximo do blast radius.",
    ["service"],
)


CRITICAL_DEPENDENCIES = Gauge(
    "dependency_critical_relationships_total",
    "Quantidade de dependências críticas.",
)