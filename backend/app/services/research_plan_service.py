from sqlalchemy.orm import Session

from app.models.research_plan import ResearchPlan
from app.services.research_planner import create_demo_plan


def create_research_plan(
    db: Session,
    task_id: int,
    prompt: str,
) -> ResearchPlan:

    plan_data = create_demo_plan(prompt)

    plan = ResearchPlan(
        task_id=task_id,
        intent=plan_data["intent"],
        summary=plan_data["summary"],
        filters=plan_data["filters"],
        fields=plan_data["fields"],
        sources=plan_data["sources"],
        workflow_steps=plan_data["workflow_steps"],
        validation_rules=plan_data["validation_rules"],
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def get_research_plan(
    db: Session,
    task_id: int,
) -> ResearchPlan | None:

    return (
        db.query(ResearchPlan)
        .filter(ResearchPlan.task_id == task_id)
        .order_by(ResearchPlan.created_at.desc())
        .first()
    )