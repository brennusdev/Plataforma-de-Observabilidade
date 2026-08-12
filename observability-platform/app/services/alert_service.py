from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.alert import AlertEvent, AlertRule
from app.models.metric import MetricSnapshot


OPERATORS = {
    ">": lambda value, threshold: value > threshold,
    ">=": lambda value, threshold: value >= threshold,
    "<": lambda value, threshold: value < threshold,
    "<=": lambda value, threshold: value <= threshold,
    "==": lambda value, threshold: value == threshold,
}


def get_metric_value(
    snapshot: MetricSnapshot,
    metric: str,
) -> float | None:

    metrics = {
        "cpu_percent": snapshot.cpu_percent,
        "memory_percent": snapshot.memory_percent,
        "disk_percent": snapshot.disk_percent,
    }

    return metrics.get(metric)


def condition_matches(
    value: float,
    operator: str,
    threshold: float,
) -> bool:

    evaluator = OPERATORS.get(operator)

    if evaluator is None:
        return False

    return evaluator(
        value,
        threshold,
    )


def has_active_alert(
    db: Session,
    rule_id: int,
) -> bool:

    alert = db.scalar(
        select(AlertEvent)
        .where(
            AlertEvent.rule_id == rule_id,
            AlertEvent.status == "active",
        )
        .order_by(
            desc(AlertEvent.created_at)
        )
        .limit(1)
    )

    return alert is not None


def evaluate_alert_rules(
    db: Session,
    snapshot: MetricSnapshot,
):

    rules = list(
        db.scalars(
            select(AlertRule)
            .where(
                AlertRule.enabled.is_(True)
            )
        )
    )

    generated_alerts = []

    for rule in rules:

        value = get_metric_value(
            snapshot,
            rule.metric,
        )

        if value is None:
            continue

        triggered = condition_matches(
            value,
            rule.operator,
            rule.threshold,
        )

        if not triggered:
            continue

        if has_active_alert(
            db,
            rule.id,
        ):
            continue

        event = AlertEvent(
            rule_id=rule.id,
            title=rule.name,
            severity=rule.severity,
            metric=rule.metric,
            value=value,
            threshold=rule.threshold,
            status="active",
        )

        db.add(event)

        generated_alerts.append(event)

    if generated_alerts:
        db.commit()

        for alert in generated_alerts:
            db.refresh(alert)

    return generated_alerts


def resolve_alerts(
    db: Session,
    snapshot: MetricSnapshot,
):

    rules = list(
        db.scalars(
            select(AlertRule)
            .where(
                AlertRule.enabled.is_(True)
            )
        )
    )

    for rule in rules:

        value = get_metric_value(
            snapshot,
            rule.metric,
        )

        if value is None:
            continue

        triggered = condition_matches(
            value,
            rule.operator,
            rule.threshold,
        )

        if triggered:
            continue

        active_alerts = list(
            db.scalars(
                select(AlertEvent)
                .where(
                    AlertEvent.rule_id == rule.id,
                    AlertEvent.status == "active",
                )
            )
        )

        for alert in active_alerts:

            alert.status = "resolved"

    db.commit()