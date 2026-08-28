"""
Rate Limiting simples baseado em janela de tempo.

Objetivo:

Evitar que um cliente consiga enviar
requisições excessivas para a API.
"""

import time

from collections import defaultdict

from fastapi import (
    Request,
)

from fastapi.responses import (
    JSONResponse,
)

from app.observability.resilience_metrics import (
    RATE_LIMIT_REJECTIONS,
)


REQUEST_LIMIT = 100

WINDOW_SECONDS = 60


_requests = defaultdict(
    list
)


async def rate_limit_middleware(
    request: Request,
    call_next,
):

    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    current_time = time.time()

    request_history = (
        _requests[client_ip]
    )

    request_history[:] = [
        timestamp
        for timestamp
        in request_history
        if current_time - timestamp
        < WINDOW_SECONDS
    ]

    if (
        len(request_history)
        >= REQUEST_LIMIT
    ):

        RATE_LIMIT_REJECTIONS.inc()

        return JSONResponse(
            status_code=429,
            content={
                "error": "rate_limit_exceeded",
                "message": (
                    "Too many requests."
                ),
            },
        )

    request_history.append(
        current_time
    )

    response = await call_next(
        request
    )

    return response