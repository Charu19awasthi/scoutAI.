from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text

from app.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    task_id = Column(
        Integer,
        ForeignKey("research_tasks.id"),
        nullable=False,
        index=True,
    )

    company = Column(
        String(255),
        nullable=True,
    )

    role = Column(
        String(255),
        nullable=True,
    )

    location = Column(
        String(255),
        nullable=True,
    )

    work_mode = Column(
        String(100),
        nullable=True,
    )

    skills = Column(
        JSON,
        nullable=True,
    )

    stipend = Column(
        String(255),
        nullable=True,
    )

    posted_date = Column(
        String(50),
        nullable=True,
    )

    application_url = Column(
        Text,
        nullable=True,
    )

    source_name = Column(
        String(255),
        nullable=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="collected",
    )

    confidence = Column(
        String(50),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
    
    evidence = relationship(
        "Evidence",
        back_populates="result",
        cascade="all, delete-orphan",
    )