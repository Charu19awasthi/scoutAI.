from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.schemas.result import ResultResponse
from app.services.data_quality_service import (
    process_results,
)


from app.services.research_executor import (
    collect_demo_results,
)

from app.services.result_service import (
    get_results_for_task,
)

from app.database import Base, engine, get_db

from app.models.research_plan import ResearchPlan
from app.models.research_task import ResearchTask
from app.models.evidence import Evidence
from app.models.result import Result

from app.schemas.research_plan import (
    ResearchPlanCreate,
    ResearchPlanResponse,
)

from app.schemas.research_task import (
    ResearchTaskCreate,
    ResearchTaskResponse,
)

from app.services.research_plan_service import (
    create_research_plan,
    get_research_plan,
)

from app.services.research_task_service import (
    create_task,
    get_all_tasks,
    get_task,
)

from app.schemas.evidence import (
    EvidenceResponse,
)

from app.services.evidence_service import (
    create_evidence_for_task,
)

# -----------------------------------
# Create database tables
# -----------------------------------

Base.metadata.create_all(bind=engine)


# -----------------------------------
# FastAPI application
# -----------------------------------

app = FastAPI(
    title="ScoutAI API",
    description=(
        "Evidence-First AI Research & "
        "Data Intelligence Platform"
    ),
    version="0.3.0",
)


# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Basic endpoints
# -----------------------------------

@app.get("/")
def root():
    return {
        "message": "ScoutAI API is running",
        "version": "0.3.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# -----------------------------------
# Research Task endpoints
# -----------------------------------

@app.post(
    "/tasks",
    response_model=ResearchTaskResponse,
)
def create_research_task(
    task_data: ResearchTaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(
        db=db,
        prompt=task_data.prompt,
    )


@app.get(
    "/tasks",
    response_model=list[ResearchTaskResponse],
)
def list_research_tasks(
    db: Session = Depends(get_db),
):
    return get_all_tasks(db)


@app.get(
    "/tasks/{task_id}",
    response_model=ResearchTaskResponse,
)
def get_research_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    return task


# -----------------------------------
# Research Plan endpoints
# -----------------------------------

@app.post(
    "/research/plan",
    response_model=ResearchPlanResponse,
)
def generate_research_plan(
    plan_data: ResearchPlanCreate,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=plan_data.task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    return create_research_plan(
        db=db,
        task_id=task.id,
        prompt=task.prompt,
    )


@app.get(
    "/research/{task_id}/plan",
    response_model=ResearchPlanResponse,
)
def get_plan(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    plan = get_research_plan(
        db=db,
        task_id=task_id,
    )

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Research plan not found",
        )

    return plan

# -----------------------------------
# Research execution
# -----------------------------------

@app.post(
    "/tasks/{task_id}/run",
    response_model=list[ResultResponse],
)
def run_research_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    results = collect_demo_results(
        db=db,
        task_id=task_id,
    )

    task.status = "completed"
    task.total_results = len(results)

    db.commit()

    return results


# -----------------------------------
# Results
# -----------------------------------

@app.get(
    "/tasks/{task_id}/results",
    response_model=list[ResultResponse],
)
def get_task_results(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    return get_results_for_task(
        db=db,
        task_id=task_id,
    )
    
    
    # -----------------------------------
# Data quality processing
# -----------------------------------

@app.post("/tasks/{task_id}/process")
def process_task_results(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    # Step 1: Clean, validate and deduplicate results
    processed_results = process_results(
        db=db,
        task_id=task_id,
    )

    # Step 2: Generate evidence for valid/review results
    evidence_records = create_evidence_for_task(
        db=db,
        task_id=task_id,
    )

    return {
        "task_id": task_id,
        "processed_results": len(processed_results),
        "evidence_records": len(evidence_records),
        "message": "Results processed and evidence generated successfully.",
    }
    
    
# -----------------------------------
# Evidence
# -----------------------------------

@app.post(
    "/tasks/{task_id}/evidence",
    response_model=list[EvidenceResponse],
)
def generate_task_evidence(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Research task not found",
        )

    return create_evidence_for_task(
        db=db,
        task_id=task_id,
    )
    
@app.get(
    "/results/{result_id}/evidence",
    response_model=list[EvidenceResponse],
)
def get_result_evidence(
    result_id: int,
    db: Session = Depends(get_db),
):
    result = (
        db.query(Result)
        .filter(
            Result.id == result_id
        )
        .first()
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found",
        )

    return (
        db.query(Evidence)
        .filter(
            Evidence.result_id == result_id
        )
        .order_by(
            Evidence.id.asc()
        )
        .all()
    )