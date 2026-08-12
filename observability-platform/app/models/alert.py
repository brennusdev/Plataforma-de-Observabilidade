from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
    )

    metric: Mapped[str] = mapped_column(
        String(50),
        index=True,
    )

    operator: Mapped[str] = mapped_column(
        String(10),
    )

    threshold: Mapped[float] = mapped_column(
        Float,
    )

    severity: Mapped[str] = mapped_column(
        String(30),
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    rule_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
    )

    severity: Mapped[str] = mapped_column(
        String(30),
    )

    metric: Mapped[str] = mapped_column(
        String(50),
    )

    value: Mapped[float] = mapped_column(
        Float,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )