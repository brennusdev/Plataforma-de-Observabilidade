from app.observability.prometheus import (
    BUSINESS_EVENTS,
)


def record_business_event(
    event: str,
):

    BUSINESS_EVENTS.labels(
        event=event
    ).inc()