"""
Métricas específicas da camada de resiliência.
"""

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)


CIRCUIT_BREAKER_FAILURES = Counter(
    "resilience_circuit_breaker_failures_total",
    "Total de falhas detectadas pelo circuit breaker.",
    [
        "service",
    ],
)


CIRCUIT_BREAKER_STATE = Gauge(
    "resilience_circuit_breaker_state",
    "Estado atual do circuit breaker.",
    [
        "service",
    ],
)


RETRY_COUNT = Counter(
    "resilience_retries_total",
    "Quantidade total de retries realizados.",
    [
        "service",
    ],
)


RATE_LIMIT_REJECTIONS = Counter(
    "resilience_rate_limit_rejections_total",
    "Requisições rejeitadas pelo rate limiter.",
)


BACKPRESSURE_ACTIVE = Gauge(
    "resilience_backpressure_active",
    "Indica se backpressure está ativo.",
)


FAILED_OPERATIONS = Counter(
    "resilience_failed_operations_total",
    "Operações que falharam após todas as tentativas.",
    [
        "service",
    ],
)


RECOVERY_TIME = Histogram(
    "resilience_recovery_time_seconds",
    "Tempo necessário para recuperação de serviços.",
    [
        "service",
    ],
)