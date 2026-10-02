from datetime import datetime, timedelta, timezone

from .models import Incident, IncidentStatus


_TITLES = (
    "Checkout response time above threshold",
    "Payment callback retries increasing",
    "Search index refresh delayed",
    "Notification queue backlog",
    "User profile image upload failure",
    "Scheduled report delivery interrupted",
    "Database replica lag detected",
    "Inventory sync missing updates",
    "Login endpoint error spike",
    "Cache eviction rate elevated",
    "Order export stalled",
    "Webhook signature rejected",
    "API gateway certificate renewal",
    "Audit event delivery delayed",
    "Background worker memory alert",
    "Dashboard widget missing data",
    "Regional health probe failure",
    "Billing reconciliation mismatch",
)
_STATUSES: tuple[IncidentStatus, ...] = ("open", "in_progress", "closed")
_SEVERITIES = ("high", "medium", "low")


def _seed(tenant: str, count: int) -> tuple[Incident, ...]:
    start = datetime(2026, 9, 15, 8, 0, tzinfo=timezone.utc)
    return tuple(
        Incident(
            id=f"{tenant}-{index + 1:03d}",
            title=f"{_TITLES[index]} ({tenant.upper()})",
            status=_STATUSES[index % len(_STATUSES)],
            severity=_SEVERITIES[index % len(_SEVERITIES)],
            created_at=start + timedelta(hours=index),
        )
        for index in range(count)
    )


INCIDENTS_BY_TENANT = {
    "alpha": _seed("alpha", 18),
    "beta": _seed("beta", 9),
}
