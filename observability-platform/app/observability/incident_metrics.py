"""
Métricas Prometheus do Incident Intelligence Engine.
"""

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)


INCIDENTS_DETECTED = Counter(
    "incident_intelligence_detected_total",
    "Total de incidentes detectados.",
)


INCIDENTS_RESOLVED = Counter(
    "incident_intelligence_resolved_total",
    "Total de incidentes resolvidos.",
)


RCA_ANALYSES = Counter(
    "incident_intelligence_rca_total",
    "Total de análises de causa raiz.",
)


RCA_CONFIDENCE = Gauge(
    "incident_intelligence_rca_confidence",
    "Confiança da hipótese de causa raiz.",
)


ACTIVE_INCIDENTS = Gauge(
    "incident_intelligence_active_incidents",
    "Quantidade de incidentes ativos.",
)


INCIDENT_DURATION = Histogram(
    "incident_intelligence_duration_seconds",
    "Duração dos incidentes.",
)