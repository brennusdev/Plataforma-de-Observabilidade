"""
Modelos SQLAlchemy para profiling.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.database import Base


class ProfilingSnapshotRecord(Base):

    __tablename__ = (
        "profiling_snapshots"
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    service: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = (
        mapped_column(
            DateTime,
            nullable=False,
        )
    )

    cpu_time: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    memory_bytes: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    hotspots: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False,
        )
    )

    memory_changes: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False,
        )
    )