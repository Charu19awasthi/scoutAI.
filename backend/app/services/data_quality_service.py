from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from app.models.result import Result
from app.models.research_task import ResearchTask


def clean_text(value: str | None) -> str | None:
    """
    Remove unnecessary spaces and normalize text.
    """

    if value is None:
        return None

    value = value.strip()

    if not value:
        return None

    # Convert multiple spaces into one space
    value = " ".join(value.split())

    return value


def normalize_work_mode(
    work_mode: str | None,
) -> str | None:
    """
    Normalize different work-mode formats.
    """

    if not work_mode:
        return None

    value = work_mode.strip().lower()

    mapping = {
        "remote": "Remote",
        "hybrid": "Hybrid",
        "on-site": "On-site",
        "onsite": "On-site",
        "on site": "On-site",
    }

    return mapping.get(
        value,
        work_mode.strip().title(),
    )


def normalize_result(result: Result) -> None:
    """
    Clean and normalize a result in-place.
    """

    result.company = clean_text(result.company)
    result.role = clean_text(result.role)
    result.location = clean_text(result.location)
    result.stipend = clean_text(result.stipend)
    result.application_url = clean_text(
        result.application_url
    )
    result.source_name = clean_text(
        result.source_name
    )

    result.work_mode = normalize_work_mode(
        result.work_mode
    )

    if result.skills:
        cleaned_skills = []

        for skill in result.skills:
            cleaned_skill = clean_text(skill)

            if cleaned_skill:
                cleaned_skills.append(
                    cleaned_skill
                )

        # Remove duplicate skills
        result.skills = list(
            dict.fromkeys(cleaned_skills)
        )


def is_valid_url(url: str | None) -> bool:
    """
    Check whether a URL has a valid HTTP/HTTPS structure.
    """

    if not url:
        return False

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def is_valid_date(
    date_value: str | None,
) -> bool:
    """
    Check whether posted_date follows YYYY-MM-DD.
    """

    if not date_value:
        return False

    try:
        datetime.strptime(
            date_value,
            "%Y-%m-%d",
        )

        return True

    except ValueError:
        return False


def validate_result(
    result: Result,
) -> list[str]:
    """
    Return a list of validation problems.
    """

    errors = []

    # Required fields
    if not result.company:
        errors.append(
            "Company is missing"
        )

    if not result.role:
        errors.append(
            "Role is missing"
        )

    if not result.location:
        errors.append(
            "Location is missing"
        )

    # URL validation
    if not is_valid_url(
        result.application_url
    ):
        errors.append(
            "Application URL is invalid"
        )

    # Date validation
    if not is_valid_date(
        result.posted_date
    ):
        errors.append(
            "Posted date is invalid"
        )

    # Source validation
    if not result.source_name:
        errors.append(
            "Source information is missing"
        )

    return errors


def create_duplicate_key(
    result: Result,
) -> str:
    """
    Create a deterministic key for duplicate detection.
    """

    company = (
        result.company or ""
    ).lower().strip()

    role = (
        result.role or ""
    ).lower().strip()

    location = (
        result.location or ""
    ).lower().strip()

    return (
        f"{company}|"
        f"{role}|"
        f"{location}"
    )


def process_results(
    db: Session,
    task_id: int,
) -> dict:

    results = (
        db.query(Result)
        .filter(
            Result.task_id == task_id
        )
        .order_by(Result.id.asc())
        .all()
    )

    seen_keys = set()

    verified_count = 0
    review_count = 0
    duplicate_count = 0

    for result in results:

        # -----------------------------
        # 1. Clean / normalize
        # -----------------------------

        normalize_result(result)

        # -----------------------------
        # 2. Validate
        # -----------------------------

        errors = validate_result(result)

        if errors:
            result.status = "review"
            result.confidence = "review"
            review_count += 1

            continue

        # -----------------------------
        # 3. Duplicate detection
        # -----------------------------

        duplicate_key = create_duplicate_key(
            result
        )

        if duplicate_key in seen_keys:
            result.status = "duplicate"
            result.confidence = "duplicate"
            duplicate_count += 1

            continue

        seen_keys.add(duplicate_key)

        # -----------------------------
        # 4. Verified result
        # -----------------------------

        result.status = "verified"
        result.confidence = "high"

        verified_count += 1

    # Update task counters
    task = (
        db.query(ResearchTask)
        .filter(
            ResearchTask.id == task_id
        )
        .first()
    )

    if task:

        task.status = "processed"

        task.total_results = len(results)

        task.verified_results = (
            verified_count
        )

        task.review_results = (
            review_count
        )

    db.commit()

    return {
        "task_id": task_id,
        "total_results": len(results),
        "verified_results": verified_count,
        "review_results": review_count,
        "duplicate_results": duplicate_count,
        "message": (
            "Results cleaned, validated "
            "and deduplicated successfully."
        ),
    }