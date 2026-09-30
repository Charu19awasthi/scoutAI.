from sqlalchemy.orm import Session

from app.models.result import Result


def get_results_for_task(
    db: Session,
    task_id: int,
) -> list[Result]:

    return (
        db.query(Result)
        .filter(
            Result.task_id == task_id,
            Result.status != "duplicate",
        )
        .order_by(Result.id.asc())
        .all()
    )


def get_all_results_for_task(
    db: Session,
    task_id: int,
) -> list[Result]:

    return (
        db.query(Result)
        .filter(
            Result.task_id == task_id
        )
        .order_by(Result.id.asc())
        .all()
    )