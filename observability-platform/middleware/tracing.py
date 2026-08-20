import time

from fastapi import Request

from opentelemetry import trace

from app.services.trace_service import (
    add_span_attribute,
    record_exception,
)


async def tracing_middleware(
    request: Request,
    call_next,
):

    tracer = trace.get_tracer(
        "observability-api"
    )

    start_time = time.perf_counter()

    route = request.url.path

    with tracer.start_as_current_span(
        "http.request"
    ) as span:

        span.set_attribute(
            "http.method",
            request.method,
        )

        span.set_attribute(
            "http.route",
            route,
        )

        span.set_attribute(
            "http.target",
            route,
        )

        try:

            response = await call_next(
                request
            )

            span.set_attribute(
                "http.status_code",
                response.status_code,
            )

            if response.status_code >= 500:

                span.set_status(
                    trace.Status(
                        trace.StatusCode.ERROR
                    )
                )

            return response

        except Exception as exc:

            record_exception(
                exc
            )

            raise

        finally:

            duration_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            add_span_attribute(
                "http.duration_ms",
                round(
                    duration_ms,
                    2,
                ),
            )