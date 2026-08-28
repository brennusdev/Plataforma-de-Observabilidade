"""
Endpoints para inspeção da resiliência.
"""

from fastapi import APIRouter

from app.observability.resilience_metrics import (
    CIRCUIT_BREAKER_STATE,
)


router = APIRouter(
    prefix="/api/resilience",
    tags=["Resilience"],
)


@router.get("/status")
def resilience_status():

    return {
        "status": "operational",
        "features": {
            "circuit_breaker": True,
            "retry": True,
            "rate_limiting": True,
            "backpressure": True,
            "idempotency": True,
            "graceful_shutdown": True,
        },
    }