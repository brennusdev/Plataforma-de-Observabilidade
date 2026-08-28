"""
Analisa os resultados dos experimentos
de Chaos Engineering.
"""


def calculate_impact_score(
    error_rate: float,
    latency_increase: float,
    availability_loss: float,
) -> float:
    """
    Calcula um score de impacto.

    Todos os valores são normalizados
    para uma escala de 0 a 100.
    """

    error_component = min(
        error_rate,
        100,
    )

    latency_component = min(
        latency_increase,
        100,
    )

    availability_component = min(
        availability_loss,
        100,
    )

    score = (
        error_component * 0.4
        + latency_component * 0.2
        + availability_component * 0.4
    )

    return round(
        score,
        2,
    )


def calculate_resilience_score(
    recovery_time: float,
    impact_score: float,
    availability: float,
) -> float:
    """
    Calcula a resiliência do sistema.

    Quanto maior:

    - disponibilidade;
    - recuperação rápida;
    - menor impacto;

    melhor será o score.
    """

    recovery_score = max(
        0,
        100 - recovery_time,
    )

    impact_score_normalized = max(
        0,
        100 - impact_score,
    )

    score = (
        availability * 0.4
        + recovery_score * 0.3
        + impact_score_normalized * 0.3
    )

    return round(
        score,
        2,
    )


def calculate_blast_radius(
    affected_services: int,
    total_services: int,
) -> float:
    """
    Calcula a porcentagem de serviços
    afetados pelo experimento.
    """

    if total_services <= 0:

        return 0

    return round(
        (
            affected_services
            / total_services
        ) * 100,
        2,
    )