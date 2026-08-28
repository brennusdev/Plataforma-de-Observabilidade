"""
Métricas Prometheus dos experimentos
de Chaos Engineering.
"""

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)


EXPERIMENTS_STARTED = Counter(
    "chaos_experiments_started_total",
    "Total de experimentos iniciados.",
)


EXPERIMENTS_COMPLETED = Counter(
    "chaos_experiments_completed_total",
    "Total de experimentos concluídos.",
)


EXPERIMENTS_FAILED = Counter(
    "chaos_experiments_failed_total",
    "Total de experimentos que falharam.",
)


EXPERIMENTS_ABORTED = Counter(
    "chaos_experiments_aborted_total",
    "Total de experimentos abortados.",
)


ACTIVE_EXPERIMENTS = Gauge(
    "chaos_active_experiments",
    "Quantidade de experimentos ativos.",
)


RECOVERY_TIME = Histogram(
    "chaos_recovery_time_seconds",
    "Tempo necessário para recuperação.",
)


IMPACT_SCORE = Gauge(
    "chaos_last_impact_score",
    "Impacto do último experimento.",
)


BLAST_RADIUS = Gauge(
    "chaos_last_blast_radius",
    "Blast radius do último experimento.",
)


RESILIENCE_SCORE = Gauge(
    "chaos_resilience_score",
    "Score de resiliência calculado.",
)