"""
Recommendation Engine.

Gera ações recomendadas com base
na hipótese de causa.
"""


def generate_recommendations(
    service: str,
    evidence: list[str],
) -> list[str]:
    """
    Gera recomendações operacionais.
    """

    recommendations = []

    evidence_text = " ".join(
        evidence
    ).lower()

    if "deployment" in evidence_text:

        recommendations.append(
            f"Inspect the latest deployment "
            f"for {service}."
        )

        recommendations.append(
            "Consider rollback if the "
            "deployment introduced the failure."
        )

    if "dependency" in evidence_text:

        recommendations.append(
            f"Inspect dependencies used by "
            f"{service}."
        )

    if "error rate" in evidence_text:

        recommendations.append(
            "Inspect application errors "
            "and recent log anomalies."
        )

    if "latency" in evidence_text:

        recommendations.append(
            "Inspect slow database queries, "
            "external APIs and resource saturation."
        )

    if not recommendations:

        recommendations.append(
            "Collect additional telemetry "
            "before taking corrective action."
        )

    return recommendations