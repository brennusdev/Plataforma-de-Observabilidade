from datetime import datetime
from pydantic import BaseModel


class MetricResponse(BaseModel):
    id: int
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    uptime_seconds: float
    created_at: datetime

    model_config = {"from_attributes": True}


class ServiceResponse(BaseModel):
    id: int
    service_name: str
    status: str
    uptime_percent: float
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertResponse(BaseModel):
    id: int
    title: str
    severity: str
    source: str
    created_at: datetime

    model_config = {"from_attributes": True}
