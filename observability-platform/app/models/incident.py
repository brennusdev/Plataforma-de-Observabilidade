"""
Modelos SQL relacionados a incidentes.
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


class IncidentRecord(Base):

    __tablename__ = "incident_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    incident_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    root_cause: Mapped[str | None] = (
        mapped_column(
            String(200),
            nullable=True,
        )
    )

    root_cause_score: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    evidence: Mapped[str | None] = (
        mapped_column(
            Text,
            nullable=True,
        )
    )

    recommendations: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            nullable=False,
        )
    )

    resolved_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime,
        nullable=True,
    )