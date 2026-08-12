from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application_metric import RequestMetric


def save_request_metric(
    db: Session,
    *,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
) -> RequestMetric:

    metric = RequestMetric(
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric


def get_request_metrics(
    db: Session,
    minutes: int = 60,
):

    since = (
        datetime.now(timezone.utc)
        - timedelta(minutes=minutes)
    )

    return list(
        db.scalars(
            select(RequestMetric)
            .where(
                RequestMetric.created_at >= since
            )
            .order_by(
                RequestMetric.created_at
            )
        )
    )


def calculate_percentile(
    values: list[float],
    percentile: float,
) -> float:

    if not values:
        return 0.0

    ordered = sorted(values)

    index = (
        percentile / 100
    ) * (
        len(ordered) - 1
    )

    lower = int(index)
    upper = lower + 1

    if upper >= len(ordered):
        return ordered[lower]

    weight = index - lower

    return (
        ordered[lower]
        + (
            ordered[upper]
            - ordered[lower]
        ) * weight
    )


def calculate_application_metrics(
    metrics: list[RequestMetric],
):

    if not metrics:

        return {
            "request_count": 0,
            "error_count": 0,
            "error_rate": 0.0,
            "average_latency_ms": 0.0,
            "p50_latency_ms": 0.0,
            "p95_latency_ms": 0.0,
            "p99_latency_ms": 0.0,
        }

    durations = [
        metric.duration_ms
        for metric in metrics
    ]

    errors = [
        metric
        for metric in metrics
        if metric.status_code >= 400
    ]

    return {
        "request_count": len(metrics),

        "error_count": len(errors),

        "error_rate": round(
            (
                len(errors)
                / len(metrics)
            ) * 100,
            2,
        ),

        "average_latency_ms": round(
            sum(durations)
            / len(durations),
            2,
        ),

        "p50_latency_ms": round(
            calculate_percentile(
                durations,
                50,
            ),
            2,
        ),

        "p95_latency_ms": round(
            calculate_percentile(
                durations,
                95,
            ),
            2,
        ),

        "p99_latency_ms": round(
            calculate_percentile(
                durations,
                99,
            ),
            2,
        ),
    }