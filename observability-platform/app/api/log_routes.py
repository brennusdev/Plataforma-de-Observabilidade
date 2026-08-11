from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.log import LogEntry
from app.schemas.logs import LogResponse


router = APIRouter(
    prefix="/api/logs",
    tags=["Logs"],
)


@router.get(
    "",
    response_model=list[LogResponse],
)
def get_logs(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),
    level: str | None = None,
    db: Session = Depends(get_db),
):

    query = select(LogEntry)

    if level:
        query = query.where(
            LogEntry.level == level.upper()
        )

    query = (
        query
        .order_by(desc(LogEntry.created_at))
        .limit(limit)
    )

    return list(db.scalars(query))