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

from prometheus_client import (
    make_asgi_app,
)

from sqlalchemy import select

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor,
)

from opentelemetry.instrumentation.sqlalchemy import (
    SQLAlchemyInstrumentor,
)

from app.api.alert_routes import (
    router as alert_router,
)

from app.api.application_metrics_routes import (
    router as application_metrics_router,
)

from app.api.health_routes import (
    router as health_router,
)

from app.api.log_routes import (
    router as log_router,
)

from app.api.resilience_routes import (
    router as resilience_router,
)

from app.api.routes import (
    router,
)

from app.api.trace_routes import (
    router as trace_router,
)

from app.core.config import settings

from app.core.database import (
    Base,
    SessionLocal,
    engine,
)
from app.api.reliability_routes import (
    router as reliability_router,
)

from middleware.correlation import (
    correlation_middleware,
)

from middleware.idempotency import (
    idempotency_middleware,
)

from middleware.logging import (
    request_logging_middleware,
)

from middleware.metrics import (
    metrics_middleware,
)

from middleware.rate_limit import (
    rate_limit_middleware,
)

from middleware.tracing import (
    tracing_middleware,
)

from app.models.alert import (
    AlertRule,
)

from app.models.metric import (
    ServiceStatus,
)

from app.observability.collector import (
    collect_system_metrics,
)

from app.observability.logging import (
    configure_logging,
)

from app.observability.retention import (
    cleanup_old_data,
)

from app.observability.tracing import (
    setup_tracing,
)

from app.services.collector_service import (
    save_snapshot,
)

from app.api.chaos_routes import (
    router as chaos_router,
)

from app.api.incident_routes import (
    router as incident_router,
)

from app.api.dependency_routes import (
    router as dependency_router,
)


configure_logging()

setup_tracing()


async def observability_loop():

    counter = 0

    while True:

        try:

            collect_system_metrics()

            with SessionLocal() as db:

                save_snapshot(
                    db
                )

            counter += 1

            if counter >= 288:

                cleanup_old_data(
                    retention_days=30
                )

                counter = 0

        except Exception as exc:

            print(
                "[observability] "
                f"error: {exc}"
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

    SQLAlchemyInstrumentor().instrument(
        engine=engine
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
                    ServiceStatus(
                        service_name="prometheus",
                        status="operational",
                        uptime_percent=99.99,
                    ),
                    ServiceStatus(
                        service_name="grafana",
                        status="operational",
                        uptime_percent=99.99,
                    ),
                    ServiceStatus(
                        service_name="otel-collector",
                        status="operational",
                        uptime_percent=99.99,
                    ),
                    ServiceStatus(
                        service_name="jaeger",
                        status="operational",
                        uptime_percent=99.99,
                    ),
                ]
            )

            db.commit()

    task = asyncio.create_task(
        observability_loop()
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
    version="8.0.0",
    lifespan=lifespan,
)


FastAPIInstrumentor.instrument_app(
    app
)


app.middleware(
    "http"
)(
    correlation_middleware
)


app.middleware(
    "http"
)(
    idempotency_middleware
)


app.middleware(
    "http"
)(
    rate_limit_middleware
)


app.middleware(
    "http"
)(
    tracing_middleware
)


app.middleware(
    "http"
)(
    request_logging_middleware
)

app.include_router(
    reliability_router
)


app.middleware(
    "http"
)(
    metrics_middleware
)

app.include_router(
    chaos_router
)


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
    incident_router
)

app.include_router(
    application_metrics_router
)

app.include_router(
    trace_router
)

app.include_router(
    health_router
)

app.include_router(
    resilience_router
)

app.include_router(
    dependency_router
)


metrics_app = make_asgi_app()


app.mount(
    "/metrics",
    metrics_app,
)


app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static",
)


@app.get("/")
def dashboard():

    return FileResponse(
        "app/static/index.html"
    )