from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResearchPlanCreate(BaseModel):
    task_id: int


class ResearchPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int

    intent: str
    summary: str

    filters: dict[str, Any]
    fields: list[str]
    sources: list[str]
    workflow_steps: list[str]
    validation_rules: list[str]

    created_at: datetime