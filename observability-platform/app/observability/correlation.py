import uuid

from contextvars import ContextVar


correlation_id_context: ContextVar[
    str
] = ContextVar(
    "correlation_id",
    default="",
)


def generate_correlation_id() -> str:

    return str(
        uuid.uuid4()
    )


def set_correlation_id(
    correlation_id: str,
):

    correlation_id_context.set(
        correlation_id
    )


def get_correlation_id() -> str:

    return correlation_id_context.get()