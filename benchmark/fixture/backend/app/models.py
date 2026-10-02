from datetime import datetime
from typing import Literal

from pydantic import BaseModel


IncidentStatus = Literal["open", "in_progress", "closed"]


class Incident(BaseModel):
    id: str
    title: str
    status: IncidentStatus
    severity: Literal["low", "medium", "high"]
    created_at: datetime


class IncidentPage(BaseModel):
    items: list[Incident]
    total: int
    page: int
    page_size: int
