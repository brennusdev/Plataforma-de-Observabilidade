from opentelemetry import trace

from app.observability.tracing import (
    tracer,
)


def create_operation_span(
    operation_name: str,
):

    return tracer.start_as_current_span(
        operation_name
    )


def add_span_attribute(
    key: str,
    value,
):

    span = trace.get_current_span()

    if span.is_recording():

        span.set_attribute(
            key,
            value,
        )


def add_span_event(
    name: str,
):

    span = trace.get_current_span()

    if span.is_recording():

        span.add_event(
            name
        )


def record_exception(
    exception: Exception,
):

    span = trace.get_current_span()

    if span.is_recording():

        span.record_exception(
            exception
        )

        span.set_status(
            trace.Status(
                trace.StatusCode.ERROR
            )
        )