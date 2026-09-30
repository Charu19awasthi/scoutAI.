import re
from typing import Any


def create_demo_plan(prompt: str) -> dict[str, Any]:
    """
    Creates a deterministic research plan from a natural-language prompt.

    This is Demo Mode.
    No external AI API is required.
    """

    prompt_lower = prompt.lower()

    # -----------------------------------
    # Detect domain / intent
    # -----------------------------------

    if any(
        word in prompt_lower
        for word in ["internship", "internships", "intern"]
    ):
        intent = "Find relevant internship opportunities"
        summary = (
            "Search for internship opportunities matching "
            "the user's requirements."
        )

        fields = [
            "company",
            "role",
            "location",
            "work_mode",
            "skills",
            "stipend",
            "posted_date",
            "application_url",
        ]

    elif any(
        word in prompt_lower
        for word in ["job", "jobs", "hiring", "vacancy"]
    ):
        intent = "Find relevant job opportunities"
        summary = (
            "Search for job opportunities matching "
            "the user's requirements."
        )

        fields = [
            "company",
            "role",
            "location",
            "work_mode",
            "skills",
            "salary",
            "posted_date",
            "application_url",
        ]

    elif any(
        word in prompt_lower
        for word in ["lead", "leads", "customer", "customers"]
    ):
        intent = "Find relevant business leads"
        summary = (
            "Research potential business leads matching "
            "the user's requirements."
        )

        fields = [
            "company",
            "contact_name",
            "industry",
            "location",
            "website",
            "contact_information",
        ]

    else:
        intent = "Perform structured web research"
        summary = (
            "Collect, structure and validate information "
            "matching the user's research requirement."
        )

        fields = [
            "name",
            "description",
            "location",
            "website",
            "source",
        ]

    # -----------------------------------
    # Detect location
    # -----------------------------------

    filters: dict[str, Any] = {}

    if "india" in prompt_lower:
        filters["country"] = "India"

    if "usa" in prompt_lower or "united states" in prompt_lower:
        filters["country"] = "United States"

    if "uk" in prompt_lower or "united kingdom" in prompt_lower:
        filters["country"] = "United Kingdom"

    # -----------------------------------
    # Detect time requirement
    # -----------------------------------

    days_match = re.search(
        r"(?:last|past|within)\s+(\d+)\s+days?",
        prompt_lower,
    )

    if days_match:
        filters["posted_within_days"] = int(
            days_match.group(1)
        )

    # -----------------------------------
    # Detect work mode
    # -----------------------------------

    work_modes = []

    if "remote" in prompt_lower:
        work_modes.append("remote")

    if "hybrid" in prompt_lower:
        work_modes.append("hybrid")

    if "on-site" in prompt_lower or "onsite" in prompt_lower:
        work_modes.append("on-site")

    if work_modes:
        filters["work_modes"] = work_modes

    # -----------------------------------
    # Detect skills
    # -----------------------------------

    known_skills = [
        "python",
        "java",
        "javascript",
        "react",
        "machine learning",
        "artificial intelligence",
        "sql",
        "aws",
        "azure",
        "docker",
        "fastapi",
    ]

    detected_skills = []

    for skill in known_skills:
        if skill in prompt_lower:
            detected_skills.append(skill)

    if detected_skills:
        filters["skills"] = detected_skills

    # -----------------------------------
    # Research workflow
    # -----------------------------------

    workflow_steps = [
        "Understand research requirement",
        "Identify permitted sources",
        "Collect source data",
        "Extract required fields",
        "Clean and normalize data",
        "Validate records",
        "Remove duplicate records",
        "Attach source evidence",
        "Prepare structured dataset",
    ]

    # -----------------------------------
    # Validation rules
    # -----------------------------------

    validation_rules = [
        "Required fields must not be empty",
        "Application URLs must be valid URLs when applicable",
        "Duplicate records should be removed",
        "Source information must be retained",
        "Results must match the requested filters",
    ]

    # -----------------------------------
    # Permitted source placeholder
    # -----------------------------------

    sources = [
        "Permitted public web sources",
        "Public company/job pages",
        "User-approved data sources",
    ]

    return {
        "intent": intent,
        "summary": summary,
        "filters": filters,
        "fields": fields,
        "sources": sources,
        "workflow_steps": workflow_steps,
        "validation_rules": validation_rules,
    }