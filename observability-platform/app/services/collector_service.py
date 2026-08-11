from sqlalchemy.orm import Session

from app.collectors.system import collect_system_metrics
from app.models.metric import MetricSnapshot


def save_snapshot(db: Session) -> MetricSnapshot:
    data = collect_system_metrics()

    snapshot = MetricSnapshot(**data)
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot
