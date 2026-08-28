"""
Chaos Engine.

Responsável por coordenar:

1. validação;
2. criação;
3. execução;
4. observação;
5. análise;
6. recuperação;
7. persistência.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.chaos.analyzer import (
    calculate_blast_radius,
    calculate_impact_score,
)

from app.chaos.executor import (
    ChaosExecutor,
)

from app.chaos.experiments import (
    ExperimentStatus,
    ExperimentType,
)

from app.chaos.recovery import (
    RecoveryTracker,
)

from app.chaos.safety import (
    ChaosSafetyPolicy,
    validate_experiment,
)

from app.models.chaos import (
    ChaosExperiment,
)

from app.observability.chaos_metrics import (
    BLAST_RADIUS,
    EXPERIMENTS_COMPLETED,
    EXPERIMENTS_FAILED,
    EXPERIMENTS_STARTED,
    IMPACT_SCORE,
    ACTIVE_EXPERIMENTS,
    RECOVERY_TIME,
)


class ChaosEngine:
    """
    Orquestrador principal.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.executor = (
            ChaosExecutor()
        )

        self.policy = (
            ChaosSafetyPolicy()
        )

    async def run_experiment(
        self,
        name: str,
        experiment_type: ExperimentType,
        target_service: str,
        duration_seconds: int,
        confirmation: bool,
    ):

        validate_experiment(
            policy=self.policy,
            duration_seconds=duration_seconds,
            confirmation=confirmation,
        )

        experiment = ChaosExperiment(
            name=name,
            experiment_type=experiment_type.value,
            target_service=target_service,
            status=ExperimentStatus.CREATED.value,
        )

        self.db.add(
            experiment
        )

        self.db.commit()

        self.db.refresh(
            experiment
        )

        EXPERIMENTS_STARTED.inc()

        ACTIVE_EXPERIMENTS.inc()

        experiment.status = (
            ExperimentStatus.RUNNING.value
        )

        experiment.started_at = (
            datetime.utcnow()
        )

        self.db.commit()

        recovery = RecoveryTracker()

        recovery.start()

        try:

            result = await (
                self.executor.execute(
                    experiment_type,
                    duration_seconds,
                )
            )

            recovery_time = (
                recovery.finish()
            )

            impact = calculate_impact_score(
                error_rate=10,
                latency_increase=20,
                availability_loss=5,
            )

            blast_radius = (
                calculate_blast_radius(
                    affected_services=1,
                    total_services=7,
                )
            )

            experiment.status = (
                ExperimentStatus.COMPLETED.value
            )

            experiment.finished_at = (
                datetime.utcnow()
            )

            experiment.recovery_time = (
                recovery_time
            )

            experiment.impact_score = (
                impact
            )

            experiment.blast_radius = (
                blast_radius
            )

            experiment.result = str(
                result
            )

            self.db.commit()

            RECOVERY_TIME.observe(
                recovery_time
            )

            IMPACT_SCORE.set(
                impact
            )

            BLAST_RADIUS.set(
                blast_radius
            )

            EXPERIMENTS_COMPLETED.inc()

            return experiment

        except Exception:

            recovery.finish()

            experiment.status = (
                ExperimentStatus.FAILED.value
            )

            experiment.finished_at = (
                datetime.utcnow()
            )

            self.db.commit()

            EXPERIMENTS_FAILED.inc()

            raise

        finally:

            ACTIVE_EXPERIMENTS.dec()