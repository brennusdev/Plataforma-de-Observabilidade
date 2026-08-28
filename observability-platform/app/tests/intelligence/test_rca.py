from datetime import datetime

from app.intelligence.incident import (
    IncidentSignal,
)

from app.intelligence.rca import (
    analyze_root_cause,
)


def test_root_cause_analysis():

    signals = [
        IncidentSignal(
            source="prometheus",
            service="api-gateway",
            signal_type="error_rate",
            value=40,
            timestamp=datetime.utcnow(),
            severity="critical",
        ),
        IncidentSignal(
            source="deployment",
            service="api-gateway",
            signal_type="deployment",
            value=1,
            timestamp=datetime.utcnow(),
            severity="critical",
        ),
    ]

    candidates = analyze_root_cause(
        signals
    )

    assert len(candidates) > 0

    assert (
        candidates[0].score
        > 0
    )