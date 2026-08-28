"""
Definição dos tipos de experimentos
disponíveis na plataforma.
"""

from enum import Enum


class ExperimentType(str, Enum):
    """
    Tipos de falhas que o Chaos Engine
    consegue simular.
    """

    API_FAILURE = "api_failure"

    CONTAINER_STOP = "container_stop"

    LATENCY_INJECTION = "latency_injection"

    CPU_STRESS = "cpu_stress"

    MEMORY_PRESSURE = "memory_pressure"

    REQUEST_FAILURE = "request_failure"


class ExperimentStatus(str, Enum):
    """
    Estados possíveis de um experimento.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    ABORTED = "aborted"