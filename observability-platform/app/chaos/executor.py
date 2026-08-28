"""
Executores dos experimentos de caos.

Nesta primeira versão não executamos
comandos destrutivos reais.

O executor funciona como uma camada
abstraída que futuramente poderá conversar
com Docker/Kubernetes.
"""

import asyncio

from app.chaos.experiments import (
    ExperimentType,
)


class ChaosExecutor:
    """
    Executa experimentos controlados.
    """

    async def execute(
        self,
        experiment_type: ExperimentType,
        duration_seconds: int,
    ):
        """
        Executa o experimento.

        Na V9 inicial usamos simulação.
        """

        if (
            experiment_type
            == ExperimentType.API_FAILURE
        ):

            return await self._simulate_api_failure(
                duration_seconds
            )

        if (
            experiment_type
            == ExperimentType.LATENCY_INJECTION
        ):

            return await self._simulate_latency(
                duration_seconds
            )

        if (
            experiment_type
            == ExperimentType.CPU_STRESS
        ):

            return await self._simulate_cpu_stress(
                duration_seconds
            )

        if (
            experiment_type
            == ExperimentType.MEMORY_PRESSURE
        ):

            return await self._simulate_memory_pressure(
                duration_seconds
            )

        if (
            experiment_type
            == ExperimentType.REQUEST_FAILURE
        ):

            return await self._simulate_request_failure(
                duration_seconds
            )

        if (
            experiment_type
            == ExperimentType.CONTAINER_STOP
        ):

            return await self._simulate_container_stop(
                duration_seconds
            )

        raise ValueError(
            "Unsupported experiment type."
        )

    async def _simulate_api_failure(
        self,
        duration: int,
    ):

        await asyncio.sleep(
            min(duration, 5)
        )

        return {
            "type": "api_failure",
            "simulated": True,
            "affected": True,
        }

    async def _simulate_latency(
        self,
        duration: int,
    ):

        await asyncio.sleep(
            min(duration, 5)
        )

        return {
            "type": "latency_injection",
            "simulated": True,
            "latency_ms": 1500,
        }

    async def _simulate_cpu_stress(
        self,
        duration: int,
    ):

        await asyncio.sleep(
            min(duration, 5)
        )

        return {
            "type": "cpu_stress",
            "simulated": True,
            "cpu_pressure": 85,
        }

    async def _simulate_memory_pressure(
        self,
        duration: int,
    ):

        await asyncio.sleep(
            min(duration, 5)
        )

        return {
            "type": "memory_pressure",
            "simulated": True,
            "memory_pressure": 80,
        }

    async def _simulate_request_failure(
        self,
        duration: int,
    ):

        await asyncio.sleep(
            min(duration, 5)
        )

        return {
            "type": "request_failure",
            "simulated": True,
            "failure_rate": 35,
        }

    async def _simulate_container_stop(
        self,
        duration: int,
    ):

        await asyncio.sleep(
            min(duration, 5)
        )

        return {
            "type": "container_stop",
            "simulated": True,
            "container_affected": True,
        }