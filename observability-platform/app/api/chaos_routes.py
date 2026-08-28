"""
API responsável pelos experimentos
de Chaos Engineering.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.chaos.engine import (
    ChaosEngine,
)

from app.chaos.experiments import (
    ExperimentType,
)

from app.core.database import (
    SessionLocal,
)


router = APIRouter(
    prefix="/api/chaos",
    tags=["Chaos Engineering"],
)


class ChaosExperimentRequest(
    BaseModel
):
    """
    Dados necessários para criar
    um experimento.
    """

    name: str = Field(
        min_length=3,
        max_length=150,
    )

    experiment_type: ExperimentType

    target_service: str

    duration_seconds: int = Field(
        default=10,
        ge=1,
        le=60,
    )

    confirmation: bool = False


@router.post(
    "/experiments"
)
async def create_experiment(
    request: ChaosExperimentRequest,
):

    with SessionLocal() as db:

        engine = ChaosEngine(
            db
        )

        try:

            experiment = (
                await engine.run_experiment(
                    name=request.name,
                    experiment_type=(
                        request.experiment_type
                    ),
                    target_service=(
                        request.target_service
                    ),
                    duration_seconds=(
                        request.duration_seconds
                    ),
                    confirmation=(
                        request.confirmation
                    ),
                )
            )

            return {
                "id": experiment.id,
                "name": experiment.name,
                "status": experiment.status,
                "target": (
                    experiment.target_service
                ),
                "impact_score": (
                    experiment.impact_score
                ),
                "blast_radius": (
                    experiment.blast_radius
                ),
                "recovery_time": (
                    experiment.recovery_time
                ),
            }

        except Exception as exc:

            raise HTTPException(
                status_code=400,
                detail=str(exc),
            )