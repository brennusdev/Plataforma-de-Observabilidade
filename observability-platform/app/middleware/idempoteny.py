"""
Middleware simples para demonstrar
controle de idempotência.

A ideia:

Se o cliente enviar o mesmo
Idempotency-Key novamente,
podemos identificar a operação
como repetida.

Nesta primeira implementação,
mantemos o armazenamento apenas
em memória.

Em uma versão posterior,
isso deverá utilizar Redis.
"""

from fastapi import Request

from fastapi.responses import (
    JSONResponse,
)


processed_requests = {}


async def idempotency_middleware(
    request: Request,
    call_next,
):

    if request.method not in {
        "POST",
        "PUT",
        "PATCH",
    }:

        return await call_next(
            request
        )

    idempotency_key = (
        request.headers.get(
            "Idempotency-Key"
        )
    )

    if not idempotency_key:

        return await call_next(
            request
        )

    if idempotency_key in (
        processed_requests
    ):

        return JSONResponse(
            status_code=409,
            content={
                "error": "duplicate_request",
                "message": (
                    "This operation "
                    "was already processed."
                ),
            },
        )

    response = await call_next(
        request
    )

    if response.status_code < 500:

        processed_requests[
            idempotency_key
        ] = True

    return response