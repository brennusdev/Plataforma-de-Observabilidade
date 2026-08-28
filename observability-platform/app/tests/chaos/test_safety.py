import pytest

from app.chaos.safety import (
    ChaosSafetyError,
    ChaosSafetyPolicy,
    validate_experiment,
)


def test_experiment_requires_confirmation():

    policy = ChaosSafetyPolicy(
        require_confirmation=True
    )

    with pytest.raises(
        ChaosSafetyError
    ):

        validate_experiment(
            policy=policy,
            duration_seconds=10,
            confirmation=False,
        )


def test_experiment_duration_limit():

    policy = ChaosSafetyPolicy(
        max_duration_seconds=30
    )

    with pytest.raises(
        ChaosSafetyError
    ):

        validate_experiment(
            policy=policy,
            duration_seconds=60,
            confirmation=True,
        )


def test_development_experiment_is_allowed():

    policy = ChaosSafetyPolicy(
        environment="development"
    )

    assert validate_experiment(
        policy=policy,
        duration_seconds=10,
        confirmation=True,
    )