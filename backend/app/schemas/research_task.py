from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearchTaskCreate(BaseModel):
    prompt: str


class ResearchTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prompt: str
    status: str

    total_results: int
    verified_results: int
    review_results: int

    error_message: str | None

    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None