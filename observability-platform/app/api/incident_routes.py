"""
Endpoints para análise inteligente de incidentes.
"""

from datetime import (
    datetime,
)

from fastapi import (
    APIRouter,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.intelligence.correlation import (
    correlate_signals,
)

from app.intelligence.incident import (
    IncidentSignal,
)

from app.intelligence.rca import (
    analyze_root_cause,
)

from app.intelligence.recommendations import (
    generate_recommendations,
)

from app.observability.incident_metrics import (
    INCIDENTS_DETECTED,
    RCA_ANALYSES,
    RCA_CONFIDENCE,
)


router = APIRouter(
    prefix="/api/incidents",
    tags=[
        "Incident Intelligence"
    ],
)


class IncidentSignalRequest(
    BaseModel
):

    source: str

    service: str

    signal_type: str

    value: float

    timestamp: datetime

    severity: str = Field(
        default="warning"
    )


class IncidentAnalysisRequest(
    BaseModel
):

    signals: list[
        IncidentSignalRequest
    ]


@router.post(
    "/analyze"
)
def analyze_incident(
    request: IncidentAnalysisRequest,
):

    signals = [
        IncidentSignal(
            source=signal.source,
            service=signal.service,
            signal_type=signal.signal_type,
            value=signal.value,
            timestamp=signal.timestamp,
            severity=signal.severity,
        )
        for signal
        in request.signals
    ]

    INCIDENTS_DETECTED.inc()

    groups = correlate_signals(
        signals
    )

    RCA_ANALYSES.inc()

    candidates = []

    for group in groups:

        candidates.extend(
            analyze_root_cause(
                group
            )
        )

    candidates.sort(
        key=lambda candidate:
        candidate.score,
        reverse=True,
    )

    if not candidates:

        return {
            "status": "insufficient_data",
            "message": (
                "Not enough correlated "
                "signals to determine "
                "a probable root cause."
            ),
        }

    root_cause = candidates[0]

    RCA_CONFIDENCE.set(
        root_cause.score
    )

    recommendations = (
        generate_recommendations(
            service=root_cause.service,
            evidence=root_cause.evidence,
        )
    )

    return {
        "status": "analyzed",
        "root_cause": {
            "service": root_cause.service,
            "score": root_cause.score,
            "reason": root_cause.reason,
            "evidence": root_cause.evidence,
        },
        "recommendations": (
            recommendations
        ),
        "correlated_groups": len(
            groups
        ),
    }