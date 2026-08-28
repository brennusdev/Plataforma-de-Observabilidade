"""
Service Level Indicators.

SLI representa aquilo que conseguimos
medir objetivamente no sistema.
"""


def calculate_availability(
    successful_requests: int,
    total_requests: int,
) -> float:
    """
    Calcula disponibilidade.

    Exemplo:

    9990 requisições bem-sucedidas
    em 10000 requisições

    = 99.9%
    """

    if total_requests <= 0:
        return 100.0

    return round(
        (
            successful_requests
            / total_requests
        ) * 100,
        4,
    )


def calculate_error_rate(
    failed_requests: int,
    total_requests: int,
) -> float:
    """
    Calcula a taxa de erro.
    """

    if total_requests <= 0:
        return 0.0

    return round(
        (
            failed_requests
            / total_requests
        ) * 100,
        4,
    )


def calculate_success_rate(
    successful_requests: int,
    total_requests: int,
) -> float:
    """
    Calcula a taxa de sucesso.
    """

    if total_requests <= 0:
        return 100.0

    return round(
        (
            successful_requests
            / total_requests
        ) * 100,
        4,
    )


def calculate_latency_percentile(
    latencies: list[float],
    percentile: float = 95,
) -> float:
    """
    Calcula um percentil de latência.

    Exemplo:

    P95 significa que 95% das requisições
    estão abaixo daquele valor.
    """

    if not latencies:
        return 0.0

    ordered = sorted(latencies)

    index = int(
        (percentile / 100)
        * len(ordered)
    )

    index = min(
        index,
        len(ordered) - 1,
    )

    return round(
        ordered[index],
        4,
    )