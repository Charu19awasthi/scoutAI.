from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class ResearchTask(Base):
    __tablename__ = "research_tasks"

    id = Column(Integer, primary_key=True, index=True)

    prompt = Column(Text, nullable=False)

    status = Column(
        String(50),
        nullable=False,
        default="created",
    )

    total_results = Column(
        Integer,
        nullable=False,
        default=0,
    )

    verified_results = Column(
        Integer,
        nullable=False,
        default=0,
    )

    review_results = Column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    started_at = Column(
        DateTime,
        nullable=True,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )