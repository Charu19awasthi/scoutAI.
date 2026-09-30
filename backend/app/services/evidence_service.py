from datetime import datetime

from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.models.result import Result


def create_evidence_for_result(
    db: Session,
    result: Result,
) -> Evidence:
    """
    Create evidence for a single research result.

    For the current demo mode, evidence is generated
    from the verified result fields already stored in
    the database.
    """

    skills_text = ""

    if result.skills:
        skills_text = ", ".join(result.skills)

    evidence_parts = []

    if result.company:
        evidence_parts.append(
            f"Company: {result.company}"
        )

    if result.role:
        evidence_parts.append(
            f"Role: {result.role}"
        )

    if result.location:
        evidence_parts.append(
            f"Location: {result.location}"
        )

    if result.work_mode:
        evidence_parts.append(
            f"Work mode: {result.work_mode}"
        )

    if skills_text:
        evidence_parts.append(
            f"Required skills: {skills_text}"
        )

    if result.stipend:
        evidence_parts.append(
            f"Stipend: {result.stipend}"
        )

    evidence_text = ". ".join(evidence_parts)

    match_reason = (
        "The result passed ScoutAI's data validation "
        "and is associated with the requested research task."
    )

    evidence = Evidence(
        result_id=result.id,
        source_name=result.source_name
        or "Unknown source",
        source_url=result.application_url
        or "",
        evidence_text=evidence_text,
        retrieved_at=datetime.utcnow(),
        verification_status=(
            "verified"
            if result.status == "verified"
            else "review"
        ),
        match_reason=match_reason,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence


def create_evidence_for_task(
    db: Session,
    task_id: int,
) -> list[Evidence]:
    """
    Create evidence for all valid results belonging
    to a research task.
    """

    results = (
        db.query(Result)
        .filter(
            Result.task_id == task_id,
            Result.status != "duplicate",
        )
        .order_by(Result.id.asc())
        .all()
    )

    evidence_records = []

    for result in results:
        existing_evidence = (
            db.query(Evidence)
            .filter(
                Evidence.result_id == result.id
            )
            .first()
        )

        if existing_evidence:
            evidence_records.append(
                existing_evidence
            )
            continue

        evidence = create_evidence_for_result(
            db=db,
            result=result,
        )

        evidence_records.append(evidence)

    return evidence_records
