from fastapi import Request

from app.observability.correlation import (
    generate_correlation_id,
    set_correlation_id,
)


async def correlation_middleware(
    request: Request,
    call_next,
):

    correlation_id = (
        request.headers.get(
            "X-Correlation-ID"
        )
    )

    if not correlation_id:

        correlation_id = (
            generate_correlation_id()
        )

    set_correlation_id(
        correlation_id
    )

    response = await call_next(
        request
    )

    response.headers[
        "X-Correlation-ID"
    ] = correlation_id

    return response