from sqlalchemy.orm import Session

from app.models.research_task import ResearchTask


def create_task(
    db: Session,
    prompt: str,
) -> ResearchTask:

    task = ResearchTask(
        prompt=prompt,
        status="created",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_all_tasks(
    db: Session,
) -> list[ResearchTask]:

    return (
        db.query(ResearchTask)
        .order_by(ResearchTask.created_at.desc())
        .all()
    )


def get_task(
    db: Session,
    task_id: int,
) -> ResearchTask | None:

    return (
        db.query(ResearchTask)
        .filter(ResearchTask.id == task_id)
        .first()
    )