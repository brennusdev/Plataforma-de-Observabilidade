"""
Endpoints da camada de Reliability Engineering.
"""

from fastapi import (
    APIRouter,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.reliability.evaluator import (
    evaluate_reliability,
)

from app.observability.reliability_metrics import (
    ERROR_BUDGET_CONSUMED,
    ERROR_BUDGET_REMAINING,
    SLI_VALUE,
    SLO_BREACH,
    SLO_TARGET,
)


router = APIRouter(
    prefix="/api/reliability",
    tags=[
        "Reliability Engineering"
    ],
)


class ReliabilityRequest(
    BaseModel
):

    service: str

    sli_value: float = Field(
        ge=0,
        le=100,
    )

    slo_target: float = Field(
        ge=0,
        le=100,
    )


@router.post(
    "/evaluate"
)
def evaluate(
    request: ReliabilityRequest,
):

    result = evaluate_reliability(
        actual_value=request.sli_value,
        slo_target=request.slo_target,
    )

    SLO_TARGET.labels(
        service=request.service
    ).set(
        request.slo_target
    )

    SLI_VALUE.labels(
        service=request.service
    ).set(
        request.sli_value
    )

    ERROR_BUDGET_CONSUMED.labels(
        service=request.service
    ).set(
        result["budget_consumed"]
    )

    ERROR_BUDGET_REMAINING.labels(
        service=request.service
    ).set(
        result["budget_remaining"]
    )

    SLO_BREACH.labels(
        service=request.service
    ).set(
        0
        if result["slo_met"]
        else 1
    )

    return {
        "service": request.service,
        **result,
    }