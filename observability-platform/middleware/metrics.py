import time

from fastapi import Request

from app.core.database import SessionLocal
from app.observability.prometheus import (
    REQUEST_COUNT,
    REQUEST_ERRORS,
    REQUEST_LATENCY,
)
from app.services.application_metric_service import (
    save_request_metric,
)


async def metrics_middleware(
    request: Request,
    call_next,
):

    start_time = time.perf_counter()

    status_code = 500

    try:

        response = await call_next(
            request
        )

        status_code = (
            response.status_code
        )

        return response

    finally:

        duration_seconds = (
            time.perf_counter()
            - start_time
        )

        duration_ms = (
            duration_seconds * 1000
        )

        path = request.url.path

        method = request.method

        REQUEST_COUNT.labels(
            method=method,
            path=path,
            status_code=str(
                status_code
            ),
        ).inc()

        REQUEST_LATENCY.labels(
            method=method,
            path=path,
        ).observe(
            duration_seconds
        )

        if status_code >= 400:

            REQUEST_ERRORS.labels(
                method=method,
                path=path,
                status_code=str(
                    status_code
                ),
            ).inc()

        try:

            with SessionLocal() as db:

                save_request_metric(
                    db,
                    method=method,
                    path=path,
                    status_code=status_code,
                    duration_ms=round(
                        duration_ms,
                        2,
                    ),
                )

        except Exception as exc:

            print(
                "[metrics] "
                f"database error: {exc}"
            )