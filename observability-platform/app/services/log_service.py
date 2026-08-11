from sqlalchemy.orm import Session

from app.models.log import LogEntry


def create_log(
    db: Session,
    *,
    level: str,
    service: str,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    message: str,
) -> LogEntry:

    log = LogEntry(
        level=level,
        service=service,
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        message=message,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log