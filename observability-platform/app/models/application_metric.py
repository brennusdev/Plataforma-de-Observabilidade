from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RequestMetric(Base):
    __tablename__ = "request_metrics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    method: Mapped[str] = mapped_column(
        String(10),
        index=True,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        index=True,
    )

    status_code: Mapped[int] = mapped_column(
        Integer,
        index=True,
    )

    duration_ms: Mapped[float] = mapped_column(
        Float,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )