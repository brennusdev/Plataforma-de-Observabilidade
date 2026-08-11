from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LogEntry(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    level: Mapped[str] = mapped_column(
        String(20),
        index=True,
        default="INFO",
    )

    service: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    method: Mapped[str] = mapped_column(
        String(10),
    )

    path: Mapped[str] = mapped_column(
        String(500),
    )

    status_code: Mapped[int] = mapped_column(
        Integer,
    )

    duration_ms: Mapped[float] = mapped_column()

    message: Mapped[str] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )