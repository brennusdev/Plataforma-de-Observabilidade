"""
Métricas Prometheus relacionadas
à confiabilidade.
"""

from prometheus_client import (
    Gauge,
)


SLO_TARGET = Gauge(
    "reliability_slo_target",
    "SLO configurado para o serviço.",
    ["service"],
)


SLI_VALUE = Gauge(
    "reliability_sli_value",
    "Valor atual do SLI.",
    ["service"],
)


ERROR_BUDGET_REMAINING = Gauge(
    "reliability_error_budget_remaining",
    "Percentual de Error Budget restante.",
    ["service"],
)


ERROR_BUDGET_CONSUMED = Gauge(
    "reliability_error_budget_consumed",
    "Percentual de Error Budget consumido.",
    ["service"],
)


SLO_BREACH = Gauge(
    "reliability_slo_breach",
    "Indica se o SLO foi violado.",
    ["service"],
)