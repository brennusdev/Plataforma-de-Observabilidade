import logging

from opentelemetry import trace

from app.observability.correlation import (
    get_correlation_id,
)


class OpenTelemetryFormatter(
    logging.Formatter
):

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:

        span = trace.get_current_span()

        span_context = (
            span.get_span_context()
        )

        if span_context.is_valid:

            trace_id = format(
                span_context.trace_id,
                "032x",
            )

            span_id = format(
                span_context.span_id,
                "016x",
            )

        else:

            trace_id = "0"

            span_id = "0"

        correlation_id = (
            get_correlation_id()
        )

        return (
            f"timestamp={self.formatTime(record)} "
            f"level={record.levelname} "
            f"trace_id={trace_id} "
            f"span_id={span_id} "
            f"correlation_id={correlation_id} "
            f"message={record.getMessage()}"
        )


def configure_logging():

    handler = logging.StreamHandler()

    handler.setFormatter(
        OpenTelemetryFormatter()
    )

    root_logger = logging.getLogger()

    root_logger.handlers.clear()

    root_logger.addHandler(
        handler
    )

    root_logger.setLevel(
        logging.INFO
    )