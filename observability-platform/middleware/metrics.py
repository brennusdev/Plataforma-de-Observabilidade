import time

from fastapi import Request

from app.core.database import SessionLocal
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

        duration_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        try:

            with SessionLocal() as db:

                save_request_metric(
                    db,
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                    duration_ms=round(
                        duration_ms,
                        2,
                    ),
                )

        except Exception as exc:

            print(
                "[metrics] "
                f"failed to save metric: {exc}"
            )