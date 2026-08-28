"""
Modelos SQL para o Dependency Graph.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
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


class ServiceRecord(Base):

    __tablename__ = "service_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    criticality: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="medium",
    )

    service_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="service",
    )

    healthy: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    version: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            default=datetime.utcnow,
        )
    )


class DependencyRecord(Base):

    __tablename__ = "dependency_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    source: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    target: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    dependency_type: Mapped[str] = (
        mapped_column(
            String(100),
            nullable=False,
            default="runtime",
        )
    )

    critical: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            default=datetime.utcnow,
        )
    )