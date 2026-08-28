"""
Mecanismos básicos de resiliência da aplicação.

A ideia deste módulo é centralizar comportamentos
relacionados à tolerância a falhas.

Nesta V8 temos:

- Circuit Breaker
- Retry
- Exponential Backoff
"""

import time

from threading import Lock

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)


class CircuitBreaker:
    """
    Implementação simples de Circuit Breaker.

    Estados:

    CLOSED
        Tudo funcionando normalmente.

    OPEN
        O sistema detectou muitas falhas e
        interrompe temporariamente as chamadas.

    HALF_OPEN
        Depois de determinado período,
        permitimos uma tentativa para descobrir
        se o serviço voltou a funcionar.
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
    ):
        self.failure_threshold = (
            failure_threshold
        )

        self.recovery_timeout = (
            recovery_timeout
        )

        self.failure_count = 0

        self.state = self.CLOSED

        self.last_failure_time = None

        self.lock = Lock()

    def can_execute(self) -> bool:
        """
        Determina se uma nova operação
        pode ser executada.
        """

        with self.lock:

            if self.state == self.CLOSED:

                return True

            if self.state == self.OPEN:

                if (
                    self.last_failure_time
                    is None
                ):
                    return False

                elapsed = (
                    time.time()
                    - self.last_failure_time
                )

                if (
                    elapsed
                    >= self.recovery_timeout
                ):

                    self.state = (
                        self.HALF_OPEN
                    )

                    return True

                return False

            return True

    def record_success(self):
        """
        Registra uma operação bem-sucedida.
        """

        with self.lock:

            self.failure_count = 0

            self.state = self.CLOSED

            self.last_failure_time = None

    def record_failure(self):
        """
        Registra uma falha.

        Quando o limite é atingido,
        o circuito é aberto.
        """

        with self.lock:

            self.failure_count += 1

            self.last_failure_time = (
                time.time()
            )

            if (
                self.failure_count
                >= self.failure_threshold
            ):

                self.state = self.OPEN


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10,
    ),
)
def resilient_operation(
    operation,
):
    """
    Executa uma operação com retry.

    Tentativas:

    1ª → imediatamente
    2ª → espera progressiva
    3ª → espera progressiva

    Se todas falharem,
    a exceção é propagada.
    """

    return operation()