import time

from fastapi import Request

from app.core.database import SessionLocal
from app.services.log_service import create_log


async def request_logging_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    status_code = 500

    try:
        response = await call_next(request)

        status_code = response.status_code

        return response

    finally:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        if status_code >= 500:
            level = "ERROR"

        elif status_code >= 400:
            level = "WARNING"

        else:
            level = "INFO"

        message = (
            f"{request.method} "
            f"{request.url.path} "
            f"-> {status_code}"
        )

        try:
            with SessionLocal() as db:

                create_log(
                    db,
                    level=level,
                    service="observability-api",
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                    duration_ms=round(
                        duration_ms,
                        2,
                    ),
                    message=message,
                )

        except Exception as exc:

            print(
                f"[logging] failed to persist log: {exc}"
            )