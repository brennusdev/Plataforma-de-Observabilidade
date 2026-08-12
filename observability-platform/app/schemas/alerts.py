from datetime import datetime

from pydantic import BaseModel, Field


class AlertRuleCreate(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=150,
    )

    metric: str

    operator: str

    threshold: float

    severity: str

    enabled: bool = True


class AlertRuleResponse(AlertRuleCreate):

    id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class AlertEventResponse(BaseModel):

    id: int

    rule_id: int

    title: str

    severity: str

    metric: str

    value: float

    threshold: float

    status: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }