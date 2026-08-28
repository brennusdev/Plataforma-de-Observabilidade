"""
Scoring Engine.

Calcula a força das evidências
associadas a uma possível causa raiz.
"""


def calculate_root_cause_score(
    temporal_correlation: float,
    service_correlation: float,
    severity: float,
    dependency_correlation: float,
    change_correlation: float,
) -> float:
    """
    Calcula um score de causa provável.

    Todos os parâmetros devem estar entre 0 e 100.

    Pesos:

    Temporal       -> 15%
    Service        -> 20%
    Severity       -> 15%
    Dependency     -> 25%
    Change         -> 25%
    """

    score = (
        temporal_correlation * 0.15
        + service_correlation * 0.20
        + severity * 0.15
        + dependency_correlation * 0.25
        + change_correlation * 0.25
    )

    return round(
        min(
            max(score, 0),
            100,
        ),
        2,
    )