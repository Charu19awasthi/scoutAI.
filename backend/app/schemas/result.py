from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int

    company: str | None
    role: str | None
    location: str | None
    work_mode: str | None

    skills: list[str] | None

    stipend: str | None
    posted_date: str | None
    application_url: str | None

    source_name: str | None
    status: str
    confidence: str | None

    created_at: datetime