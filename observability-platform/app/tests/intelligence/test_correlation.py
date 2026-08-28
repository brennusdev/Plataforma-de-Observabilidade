from datetime import (
    datetime,
    timedelta,
)

from app.intelligence.correlation import (
    correlate_signals,
)

from app.intelligence.incident import (
    IncidentSignal,
)


def test_related_signals_are_grouped():

    now = datetime.utcnow()

    signals = [
        IncidentSignal(
            source="prometheus",
            service="api",
            signal_type="error_rate",
            value=20,
            timestamp=now,
        ),
        IncidentSignal(
            source="prometheus",
            service="api",
            signal_type="latency",
            value=500,
            timestamp=(
                now
                + timedelta(
                    seconds=30
                )
            ),
        ),
    ]

    groups = correlate_signals(
        signals
    )

    assert len(groups) == 1

    assert len(groups[0]) == 2