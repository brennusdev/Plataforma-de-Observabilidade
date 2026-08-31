"""
Profiling Analyzer.

Identifica possíveis gargalos
e classifica sua severidade.
"""

from app.profiling.snapshot import (
    ProfilingSnapshot,
)


def analyze_snapshot(
    snapshot: ProfilingSnapshot,
) -> dict:
    """
    Analisa um snapshot de profiling.
    """

    hotspots = snapshot.hotspots

    top_hotspot = (
        hotspots[0]
        if hotspots
        else None
    )

    if top_hotspot is None:

        return {
            "status": "no_data",
            "service": snapshot.service,
        }

    cpu_percentage = calculate_cpu_percentage(
        hotspots
    )

    severity = classify_hotspot(
        cpu_percentage
    )

    return {
        "status": "analyzed",
        "service": snapshot.service,
        "timestamp": snapshot.timestamp,
        "memory_bytes": snapshot.memory_bytes,
        "top_hotspot": top_hotspot,
        "cpu_percentage": cpu_percentage,
        "severity": severity,
        "recommendation": (
            generate_recommendation(
                severity
            )
        ),
    }


def calculate_cpu_percentage(
    hotspots: list[dict],
) -> float:
    """
    Estima a concentração de CPU
    do hotspot dominante.
    """

    if not hotspots:

        return 0.0

    total = sum(
        item["cumulative_time"]
        for item in hotspots
    )

    if total <= 0:

        return 0.0

    top = hotspots[0][
        "cumulative_time"
    ]

    return round(
        (top / total) * 100,
        2,
    )


def classify_hotspot(
    percentage: float,
) -> str:
    """
    Classifica a concentração
    do hotspot.
    """

    if percentage >= 70:

        return "critical"

    if percentage >= 50:

        return "high"

    if percentage >= 30:

        return "medium"

    return "low"


def generate_recommendation(
    severity: str,
) -> str:
    """
    Gera uma recomendação operacional.
    """

    recommendations = {
        "critical": (
            "Investigate the dominant "
            "CPU hotspot immediately."
        ),
        "high": (
            "Review the dominant function "
            "for optimization opportunities."
        ),
        "medium": (
            "Monitor the hotspot and "
            "evaluate optimization."
        ),
        "low": (
            "No immediate optimization "
            "required."
        ),
    }

    return recommendations.get(
        severity,
        "Collect additional profiling data.",
    )