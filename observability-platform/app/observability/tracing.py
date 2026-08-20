from opentelemetry import trace

from opentelemetry.sdk.resources import (
    Resource,
)

from opentelemetry.sdk.trace import (
    TracerProvider,
)

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)


def setup_tracing() -> TracerProvider:

    resource = Resource.create(
        {
            "service.name": "observability-api",
            "service.version": "6.0.0",
            "deployment.environment": "development",
        }
    )

    provider = TracerProvider(
        resource=resource
    )

    exporter = OTLPSpanExporter(
        endpoint="otel-collector:4317",
        insecure=True,
    )

    processor = BatchSpanProcessor(
        exporter
    )

    provider.add_span_processor(
        processor
    )

    trace.set_tracer_provider(
        provider
    )

    return provider


tracer = trace.get_tracer(
    "observability-api"
)