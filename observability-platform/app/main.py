import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.api.log_routes import router as log_router
from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from middleware.logging import request_logging_middleware
from app.models.log import LogEntry
from app.models.metric import Alert, MetricSnapshot, ServiceStatus
from app.services.collector_service import save_snapshot


async def collector_loop():

    while True:

        try:

            with SessionLocal() as db:

                snapshot = save_snapshot(db)

                if snapshot.cpu_percent >= 90:

                    with SessionLocal() as alert_db:

                        alert_db.add(
                            Alert(
                                title="High CPU Usage",
                                severity="critical",
                                source="system",
                            )
                        )

                        alert_db.commit()

        except Exception as exc:

            print(
                f"[collector] error: {exc}"
            )

        await asyncio.sleep(
            settings.collect_interval_seconds
        )


@asynccontextmanager
async def lifespan(app: FastAPI):

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
    version="2.0.0",
    lifespan=lifespan,
)


app.middleware(
    "http"
)(
    request_logging_middleware
)


app.include_router(router)

app.include_router(
    log_router
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
        "version": "2.0.0",
    }


@app.get("/")
def dashboard():

    return FileResponse(
        "app/static/index.html"
    )
