from sqlalchemy.orm import Session

from app.collectors.system import collect_system_metrics
from app.models.metric import MetricSnapshot
from app.services.alert_service import (
    evaluate_alert_rules,
    resolve_alerts,
)


def save_snapshot(
    db: Session,
) -> MetricSnapshot:

    data = collect_system_metrics()

    snapshot = MetricSnapshot(
        **data
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    evaluate_alert_rules(
        db,
        snapshot,
    )

    resolve_alerts(
        db,
        snapshot,
    )

    return snapshot
