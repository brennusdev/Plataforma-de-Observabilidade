"""
Root Cause Analysis Engine.

Transforma sinais correlacionados
em hipóteses de causa.
"""

from dataclasses import dataclass

from app.intelligence.incident import (
    IncidentSignal,
)

from app.intelligence.scoring import (
    calculate_root_cause_score,
)


@dataclass
class RootCauseCandidate:
    """
    Possível causa raiz.
    """

    service: str

    reason: str

    score: float

    evidence: list[str]


def analyze_root_cause(
    signals: list[IncidentSignal],
) -> list[RootCauseCandidate]:
    """
    Analisa sinais e produz hipóteses
    de causa raiz.

    Esta versão utiliza regras explícitas.
    """

    candidates = []

    services = set(
        signal.service
        for signal in signals
    )

    for service in services:

        service_signals = [
            signal
            for signal in signals
            if signal.service
            == service
        ]

        has_error = any(
            signal.signal_type
            == "error_rate"
            for signal in service_signals
        )

        has_latency = any(
            signal.signal_type
            == "latency"
            for signal in service_signals
        )

        has_deployment = any(
            signal.signal_type
            == "deployment"
            for signal in service_signals
        )

        has_dependency_failure = any(
            signal.signal_type
            == "dependency_failure"
            for signal in service_signals
        )

        evidence = []

        if has_error:

            evidence.append(
                "Error rate increased."
            )

        if has_latency:

            evidence.append(
                "Latency increased."
            )

        if has_deployment:

            evidence.append(
                "A deployment occurred "
                "near the incident."
            )

        if has_dependency_failure:

            evidence.append(
                "A dependency reported "
                "a failure."
            )

        temporal = 80 if (
            has_deployment
        ) else 50

        service_score = min(
            len(service_signals) * 20,
            100,
        )

        severity = max(
            [
                _severity_score(
                    signal.severity
                )
                for signal
                in service_signals
            ],
            default=0,
        )

        dependency = (
            100
            if has_dependency_failure
            else 20
        )

        change = (
            100
            if has_deployment
            else 20
        )

        score = calculate_root_cause_score(
            temporal_correlation=temporal,
            service_correlation=service_score,
            severity=severity,
            dependency_correlation=dependency,
            change_correlation=change,
        )

        candidates.append(
            RootCauseCandidate(
                service=service,
                reason=(
                    "Multiple correlated signals "
                    "were detected."
                ),
                score=score,
                evidence=evidence,
            )
        )

    return sorted(
        candidates,
        key=lambda candidate:
        candidate.score,
        reverse=True,
    )


def _severity_score(
    severity: str,
) -> float:
    """
    Converte severidade textual
    em valor numérico.
    """

    values = {
        "info": 20,
        "warning": 50,
        "critical": 100,
    }

    return values.get(
        severity.lower(),
        0,
    )