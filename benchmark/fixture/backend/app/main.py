from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Query

from .data import INCIDENTS_BY_TENANT
from .models import IncidentPage


app = FastAPI(title="Incident Desk", version="1.0.0")


@app.get("/api/incidents", response_model=IncidentPage)
def list_incidents(
    x_tenant_id: Annotated[str | None, Header()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 5,
) -> IncidentPage:
    if x_tenant_id is None or x_tenant_id not in INCIDENTS_BY_TENANT:
        raise HTTPException(status_code=401, detail="Unknown tenant")

    incidents = sorted(
        INCIDENTS_BY_TENANT[x_tenant_id],
        key=lambda incident: incident.created_at,
        reverse=True,
    )
    offset = (page - 1) * page_size
    return IncidentPage(
        items=incidents[offset : offset + page_size],
        total=len(incidents),
        page=page,
        page_size=page_size,
    )
