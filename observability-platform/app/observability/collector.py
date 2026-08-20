import psutil

from app.observability.prometheus import (
    APPLICATION_INFO,
    APPLICATION_UP,
    CPU_USAGE,
    DISK_USAGE,
    MEMORY_USAGE,
)


def collect_system_metrics():

    CPU_USAGE.set(
        psutil.cpu_percent(
            interval=None
        )
    )

    MEMORY_USAGE.set(
        psutil.virtual_memory().percent
    )

    DISK_USAGE.set(
        psutil.disk_usage("/").percent
    )

    APPLICATION_INFO.labels(
        service="observability-api",
        version="7.0.0",
        environment="development",
    ).set(1)

    APPLICATION_UP.set(1)