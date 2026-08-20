import time

from fastapi import Request

from app.observability.prometheus import (
    ACTIVE_REQUESTS,
    REQUEST_COUNT,
    REQUEST_ERRORS,
    REQUEST_LATENCY,
)


async def metrics_middleware(
    request: Request,
    call_next,
):

    start_time = time.perf_counter()

    ACTIVE_REQUESTS.inc()

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

        route = (
            request.scope.get(
                "route"
            )
        )

        if route:

            route_path = (
                getattr(
                    route,
                    "path",
                    request.url.path,
                )
            )

        else:

            route_path = "unknown"

        method = request.method

        REQUEST_COUNT.labels(
            method=method,
            route=route_path,
            status_code=str(
                status_code
            ),
        ).inc()

        REQUEST_LATENCY.labels(
            method=method,
            route=route_path,
        ).observe(
            duration_seconds
        )

        if status_code >= 400:

            REQUEST_ERRORS.labels(
                method=method,
                route=route_path,
                status_code=str(
                    status_code
                ),
            ).inc()

        ACTIVE_REQUESTS.dec()