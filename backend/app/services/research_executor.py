import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.models.result import Result


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample"
    / "internships.json"
)


def load_demo_data() -> list[dict[str, Any]]:
    """Load ScoutAI demo research data."""

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def collect_demo_results(
    db: Session,
    task_id: int,
) -> list[Result]:

    records = load_demo_data()

    results = []

    for record in records:
        result = Result(
            task_id=task_id,
            company=record.get("company"),
            role=record.get("role"),
            location=record.get("location"),
            work_mode=record.get("work_mode"),
            skills=record.get("skills", []),
            stipend=record.get("stipend"),
            posted_date=record.get("posted_date"),
            application_url=record.get("application_url"),
            source_name=record.get("source_name"),
            status="collected",
            confidence="demo",
        )

        db.add(result)
        results.append(result)

    db.commit()

    for result in results:
        db.refresh(result)

    return results