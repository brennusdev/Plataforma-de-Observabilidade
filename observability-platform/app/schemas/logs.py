from datetime import datetime

from pydantic import BaseModel


class LogResponse(BaseModel):
    id: int
    level: str
    service: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    message: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }