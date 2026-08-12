from app.api.alert_routes import (
    router as alert_router,
)

from app.api.log_routes import (
    router as log_router,
)

from app.api.routes import (
    router,
)


__all__ = [
    "router",
    "log_router",
    "alert_router",
]