from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    result_id = Column(
        Integer,
        ForeignKey("results.id"),
        nullable=False,
    )

    source_name = Column(
        String,
        nullable=False,
    )

    source_url = Column(
        String,
        nullable=False,
    )

    evidence_text = Column(
        Text,
        nullable=True,
    )

    retrieved_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    verification_status = Column(
        String,
        default="verified",
        nullable=False,
    )

    match_reason = Column(
        Text,
        nullable=True,
    )

    result = relationship(
        "Result",
        back_populates="evidence",
    )