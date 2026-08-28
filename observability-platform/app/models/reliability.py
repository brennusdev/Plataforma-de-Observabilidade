"""
Modelos persistentes de Reliability Engineering.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.database import Base


class SLORecord(Base):

    __tablename__ = "slo_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    indicator: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    window_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            default=datetime.utcnow,
        )
    )


class ReliabilitySnapshot(Base):

    __tablename__ = "reliability_snapshots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    service: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    sli_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    slo_target: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    budget_consumed: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    budget_remaining: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            default=datetime.utcnow,
        )
    )