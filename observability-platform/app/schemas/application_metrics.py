from pydantic import BaseModel


class ApplicationMetricsResponse(
    BaseModel
):

    request_count: int

    error_count: int

    error_rate: float

    average_latency_ms: float

    p50_latency_ms: float

    p95_latency_ms: float

    p99_latency_ms: float