from app.api.alert_routes import (
    router as alert_router,
)

from app.api.application_metrics_routes import (
    router as application_metrics_router,
)

from app.api.health_routes import (
    router as health_router,
)

from app.api.log_routes import (
    router as log_router,
)

from app.api.routes import (
    router,
)

from app.api.trace_routes import (
    router as trace_router,
)


__all__ = [
    "router",
    "alert_router",
    "application_metrics_router",
    "health_router",
    "log_router",
    "trace_router",
]