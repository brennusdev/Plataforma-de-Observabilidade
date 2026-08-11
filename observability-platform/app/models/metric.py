from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cpu_percent: Mapped[float] = mapped_column(Float)
    memory_percent: Mapped[float] = mapped_column(Float)
    disk_percent: Mapped[float] = mapped_column(Float)
    uptime_seconds: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class ServiceStatus(Base):
    __tablename__ = "service_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(30))
    uptime_percent: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    severity: Mapped[str] = mapped_column(String(30))
    source: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
