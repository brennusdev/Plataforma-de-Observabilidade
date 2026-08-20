from fastapi import APIRouter

from opentelemetry import trace


router = APIRouter(
    prefix="/api/traces",
    tags=["Tracing"],
)


@router.get(
    "/current",
)
def current_trace():

    span = trace.get_current_span()

    context = span.get_span_context()

    if not context.is_valid:

        return {
            "trace_id": None,
            "span_id": None,
            "valid": False,
        }

    return {
        "trace_id": format(
            context.trace_id,
            "032x",
        ),
        "span_id": format(
            context.span_id,
            "016x",
        ),
        "valid": True,
    }