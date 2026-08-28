"""
Camada de segurança do Chaos Engine.

O objetivo é impedir experimentos perigosos
ou executados fora dos ambientes permitidos.
"""

from dataclasses import dataclass


@dataclass
class ChaosSafetyPolicy:
    """
    Define as regras de segurança.
    """

    environment: str = "development"

    max_duration_seconds: int = 60

    allow_production: bool = False

    require_confirmation: bool = True


class ChaosSafetyError(Exception):
    """
    Exceção utilizada quando uma operação
    viola uma política de segurança.
    """


def validate_experiment(
    policy: ChaosSafetyPolicy,
    duration_seconds: int,
    confirmation: bool,
):
    """
    Valida se um experimento pode ser executado.
    """

    if (
        duration_seconds
        > policy.max_duration_seconds
    ):
        raise ChaosSafetyError(
            "Experiment duration exceeds "
            "the configured safety limit."
        )

    if (
        policy.environment == "production"
        and not policy.allow_production
    ):
        raise ChaosSafetyError(
            "Chaos experiments are disabled "
            "in production."
        )

    if (
        policy.require_confirmation
        and not confirmation
    ):
        raise ChaosSafetyError(
            "Explicit experiment confirmation "
            "is required."
        )

    return True