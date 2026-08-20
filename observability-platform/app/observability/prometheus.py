from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests.",
    [
        "method",
        "route",
        "status_code",
    ],
)


REQUEST_ERRORS = Counter(
    "http_request_errors_total",
    "Total HTTP request errors.",
    [
        "method",
        "route",
        "status_code",
    ],
)


REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency.",
    [
        "method",
        "route",
    ],
    buckets=[
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
    ],
)


CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "Current CPU usage percentage.",
)


MEMORY_USAGE = Gauge(
    "system_memory_usage_percent",
    "Current memory usage percentage.",
)


DISK_USAGE = Gauge(
    "system_disk_usage_percent",
    "Current disk usage percentage.",
)


APPLICATION_UP = Gauge(
    "application_up",
    "Application availability.",
)


APPLICATION_INFO = Gauge(
    "application_info",
    "Application information.",
    [
        "service",
        "version",
        "environment",
    ],
)


ACTIVE_REQUESTS = Gauge(
    "http_active_requests",
    "Current active HTTP requests.",
)


BUSINESS_EVENTS = Counter(
    "application_business_events_total",
    "Total application business events.",
    [
        "event",
    ],
)