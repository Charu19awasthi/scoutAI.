from datetime import datetime

from pydantic import BaseModel


class EvidenceBase(BaseModel):
    source_name: str
    source_url: str
    evidence_text: str | None = None
    verification_status: str = "verified"
    match_reason: str | None = None


class EvidenceCreate(EvidenceBase):
    result_id: int


class EvidenceResponse(EvidenceBase):
    id: int
    result_id: int
    retrieved_at: datetime

    class Config:
        from_attributes = True