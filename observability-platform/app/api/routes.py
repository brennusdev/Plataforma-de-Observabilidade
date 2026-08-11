from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.metric import Alert, MetricSnapshot, ServiceStatus
from app.schemas.metrics import AlertResponse, MetricResponse, ServiceResponse
from app.services.collector_service import save_snapshot


router = APIRouter(prefix="/api", tags=["Observability"])


@router.get("/metrics/latest", response_model=MetricResponse)
def latest_metrics(db: Session = Depends(get_db)):
    metric = db.scalar(
        select(MetricSnapshot).order_by(desc(MetricSnapshot.created_at)).limit(1)
    )

    if metric is None:
        metric = save_snapshot(db)

    return metric


@router.get("/metrics/history", response_model=list[MetricResponse])
def metric_history(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 500))

    return list(
        db.scalars(
            select(MetricSnapshot)
            .order_by(desc(MetricSnapshot.created_at))
            .limit(limit)
        )
    )


@router.get("/services", response_model=list[ServiceResponse])
def services(db: Session = Depends(get_db)):
    return list(
        db.scalars(
            select(ServiceStatus)
            .order_by(desc(ServiceStatus.created_at))
            .limit(20)
        )
    )


@router.get("/alerts", response_model=list[AlertResponse])
def alerts(db: Session = Depends(get_db)):
    return list(
        db.scalars(
            select(Alert)
            .order_by(desc(Alert.created_at))
            .limit(20)
        )
    )


@router.post("/metrics/collect", response_model=MetricResponse)
def collect_now(db: Session = Depends(get_db)):
    return save_snapshot(db)
