from datetime import datetime
from datetime import timedelta
from datetime import timezone

from sqlalchemy import delete

from app.core.database import (
    SessionLocal,
)

from app.models.application_metric import (
    RequestMetric,
)

from app.models.log import (
    LogEntry,
)


def cleanup_old_data(
    retention_days: int = 30,
):

    cutoff = (
        datetime.now(
            timezone.utc
        )
        - timedelta(
            days=retention_days
        )
    )

    with SessionLocal() as db:

        db.execute(
            delete(
                RequestMetric
            ).where(
                RequestMetric.created_at
                < cutoff
            )
        )

        db.execute(
            delete(
                LogEntry
            ).where(
                LogEntry.created_at
                < cutoff
            )
        )

        db.commit()