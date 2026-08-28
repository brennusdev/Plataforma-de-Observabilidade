"""
Medição da recuperação do sistema.
"""

import time


class RecoveryTracker:
    """
    Controla o início e o fim
    de um processo de recuperação.
    """

    def __init__(self):

        self.started_at = None

    def start(self):

        self.started_at = time.perf_counter()

    def finish(self) -> float:
        """
        Retorna o tempo de recuperação
        em segundos.
        """

        if self.started_at is None:

            return 0.0

        elapsed = (
            time.perf_counter()
            - self.started_at
        )

        self.started_at = None

        return round(
            elapsed,
            4,
        )