import asyncio

from contextlib import (
    asynccontextmanager,
    suppress,
)

from fastapi import FastAPI

from fastapi.responses import (
    FileResponse,
)

from fastapi.staticfiles import (
    StaticFiles,
)

from sqlalchemy import select

from app.api.alert_routes import (
    router as alert_router,
)

from app.api.application_metrics_routes import (
    router as application_metrics_router,
)

from app.api.log_routes import (
    router as log_router,
)

from app.api.routes import (
    router,
)

from app.core.config import settings

from app.core.database import (
    Base,
    SessionLocal,
    engine,
)

from app.models.alert import (
    AlertRule,
)

from app.models.metric import (
    ServiceStatus,
)

from app.services.collector_service import (
    save_snapshot,
)


# Note: metrics middleware imports removed - module not found
# Uncomment middleware registration below once middleware is implemented


async def collector_loop():

    while True:

        try:

            with SessionLocal() as db:

                save_snapshot(
                    db
                )

        except Exception as exc:

            print(
                f"[collector] error: {exc}"
            )

        await asyncio.sleep(
            settings.collect_interval_seconds
        )


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    Base.metadata.create_all(
        bind=engine
    )

    with SessionLocal() as db:

        if db.scalar(
            select(ServiceStatus).limit(1)
        ) is None:

            db.add_all(
                [
                    ServiceStatus(
                        service_name="api-gateway",
                        status="operational",
                        uptime_percent=99.95,
                    ),

                    ServiceStatus(
                        service_name="database",
                        status="operational",
                        uptime_percent=99.99,
                    ),

                    ServiceStatus(
                        service_name="collector",
                        status="operational",
                        uptime_percent=99.90,
                    ),
                ]
            )

            db.commit()

        if db.scalar(
            select(AlertRule).limit(1)
        ) is None:

            db.add_all(
                [
                    AlertRule(
                        name="High CPU Usage",
                        metric="cpu_percent",
                        operator=">=",
                        threshold=90,
                        severity="critical",
                    ),

                    AlertRule(
                        name="High Memory Usage",
                        metric="memory_percent",
                        operator=">=",
                        threshold=85,
                        severity="warning",
                    ),

                    AlertRule(
                        name="Low Disk Capacity",
                        metric="disk_percent",
                        operator=">=",
                        threshold=90,
                        severity="critical",
                    ),
                ]
            )

            db.commit()

    task = asyncio.create_task(
        collector_loop()
    )

    try:

        yield

    finally:

        task.cancel()

        with suppress(
            asyncio.CancelledError
        ):

            await task


app = FastAPI(
    title=settings.app_name,
    version="4.0.0",
    lifespan=lifespan,
)


# Middleware registrations commented out - functions not yet implemented
# app.middleware(
#     "http"
# )(
#     request_logging_middleware
# )
#
#
# app.middleware(
#     "http"
# )(
#     metrics_middleware
# )


app.include_router(
    router
)


app.include_router(
    log_router
)


app.include_router(
    alert_router
)


app.include_router(
    application_metrics_router
)


app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static",
)


@app.get("/health")
def health():

    return {
        "status": "operational",
        "service": settings.app_name,
        "version": "4.0.0",
    }


@app.get("/")
def dashboard():

    return FileResponse(
        "app/static/index.html"
    )