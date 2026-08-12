from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import AlertEvent, AlertRule
from app.schemas.alerts import (
    AlertEventResponse,
    AlertRuleCreate,
    AlertRuleResponse,
)


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alert Engine"],
)


@router.post(
    "/rules",
    response_model=AlertRuleResponse,
)
def create_alert_rule(
    data: AlertRuleCreate,
    db: Session = Depends(get_db),
):

    existing = db.scalar(
        select(AlertRule)
        .where(
            AlertRule.name == data.name
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Alert rule already exists.",
        )

    rule = AlertRule(
        name=data.name,
        metric=data.metric,
        operator=data.operator,
        threshold=data.threshold,
        severity=data.severity,
        enabled=data.enabled,
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


@router.get(
    "/rules",
    response_model=list[AlertRuleResponse],
)
def get_alert_rules(
    db: Session = Depends(get_db),
):

    return list(
        db.scalars(
            select(AlertRule)
            .order_by(
                desc(AlertRule.created_at)
            )
        )
    )


@router.get(
    "/events",
    response_model=list[AlertEventResponse],
)
def get_alert_events(
    db: Session = Depends(get_db),
):

    return list(
        db.scalars(
            select(AlertEvent)
            .order_by(
                desc(AlertEvent.created_at)
            )
            .limit(100)
        )
    )


@router.get(
    "/active",
    response_model=list[AlertEventResponse],
)
def get_active_alerts(
    db: Session = Depends(get_db),
):

    return list(
        db.scalars(
            select(AlertEvent)
            .where(
                AlertEvent.status == "active"
            )
            .order_by(
                desc(AlertEvent.created_at)
            )
        )
    )