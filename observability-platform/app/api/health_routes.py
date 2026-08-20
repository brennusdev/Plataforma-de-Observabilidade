from fastapi import APIRouter

from sqlalchemy import text

from app.core.database import (
    SessionLocal,
)

from app.observability.prometheus import (
    APPLICATION_UP,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():

    return {
        "status": "operational",
        "service": "observability-api",
    }


@router.get("/live")
def liveness():

    return {
        "status": "alive",
    }


@router.get("/ready")
def readiness():

    try:

        with SessionLocal() as db:

            db.execute(
                text("SELECT 1")
            )

        APPLICATION_UP.set(1)

        return {
            "status": "ready",
            "database": "available",
        }

    except Exception:

        APPLICATION_UP.set(0)

        return {
            "status": "not_ready",
            "database": "unavailable",
        }


@router.get("/startup")
def startup():

    return {
        "status": "started",
    }