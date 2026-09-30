from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, Text

from app.database import Base


class ResearchPlan(Base):
    __tablename__ = "research_plans"

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

    intent = Column(
        Text,
        nullable=False,
    )

    summary = Column(
        Text,
        nullable=False,
    )

    filters = Column(
        JSON,
        nullable=False,
        default=dict,
    )

    fields = Column(
        JSON,
        nullable=False,
        default=list,
    )

    sources = Column(
        JSON,
        nullable=False,
        default=list,
    )

    workflow_steps = Column(
        JSON,
        nullable=False,
        default=list,
    )

    validation_rules = Column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )