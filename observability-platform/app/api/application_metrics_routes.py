from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.application_metrics import (
    ApplicationMetricsResponse,
)
from app.services.application_metric_service import (
    calculate_application_metrics,
    get_request_metrics,
)


router = APIRouter(
    prefix="/api/application",
    tags=["Application Metrics"],
)


@router.get(
    "/metrics",
    response_model=ApplicationMetricsResponse,
)
def application_metrics(
    minutes: int = Query(
        default=60,
        ge=1,
        le=1440,
    ),
    db: Session = Depends(get_db),
):

    metrics = get_request_metrics(
        db,
        minutes,
    )

    return calculate_application_metrics(
        metrics
    )