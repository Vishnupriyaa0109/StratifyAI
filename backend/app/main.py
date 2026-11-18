import os
from datetime import datetime, timezone
from collections import Counter
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from .analysis import analyze_feedback
from .analytics import compute_product_metrics
from .database import Base, engine, get_db
from .models import Experiment, Feedback, Opportunity, ProductEvent
from .schemas import (
    ExperimentCreate, ExperimentStatusUpdate, FeedbackCreate,
    FeedbackOut, OpportunityCreate, OpportunityStatusUpdate, ProductEventCreate,
)
from .seed import seed_demo_data, seed_product_events

app = FastAPI(
    title="StratifyAI API",
    description="Customer feedback intelligence and product decision workspace",
    version="0.1.0",
)

origins = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_demo_data(db)
        seed_product_events(db)


@app.get("/")
def root():
    return {"name": "StratifyAI API", "status": "online", "version": app.version}


@app.get("/health")
def health():
    return {"status": "healthy"}


def record_product_event(db: Session, event_name: str, properties: dict | None = None):
    """Record an action in the local demo workspace event stream."""
    workspace_id = "local-demo-workspace"
    has_signup = db.scalar(
        select(ProductEvent.id).where(
            ProductEvent.workspace_id == workspace_id,
            ProductEvent.event_name == "workspace_created",
        ).limit(1)
    )
    now = datetime.now(timezone.utc)
    if not has_signup:
        db.add(ProductEvent(
            event_name="workspace_created",
            workspace_id=workspace_id,
            event_properties={"source": "local_application"},
            is_synthetic=False,
            occurred_at=now,
        ))
    db.add(ProductEvent(
        event_name=event_name,
        workspace_id=workspace_id,
        event_properties=properties or {},
        is_synthetic=False,
        occurred_at=now,
    ))
    db.commit()


@app.get("/api/metrics/overview")
def product_metrics(db: Session = Depends(get_db)):
    """Return activation, engagement, retention, and funnel metrics."""
    events = list(db.scalars(select(ProductEvent)))
    return compute_product_metrics(events)


@app.get("/api/metrics/event-taxonomy")
def product_event_taxonomy():
    return {
        "events": [
            {"name": "workspace_created", "description": "A workspace is created"},
            {"name": "feedback_created", "description": "A feedback signal is captured"},
            {"name": "insight_reviewed", "description": "A human reviews a suggested insight"},
            {"name": "opportunity_created", "description": "A customer problem is added to the opportunity backlog"},
            {"name": "opportunity_prioritized", "description": "An opportunity is promoted for planned or active work"},
            {"name": "experiment_created", "description": "A testable product hypothesis is recorded"},
            {"name": "experiment_completed", "description": "An experiment is marked completed"},
            {"name": "workspace_active", "description": "A workspace performs a meaningful product action"},
        ],
        "required_context": ["workspace_id", "occurred_at"],
        "optional_context": ["actor_id", "properties"],
        "privacy_note": "Do not send names, email addresses, free-text customer feedback, or other personal data as event properties.",
    }


@app.post("/api/events", status_code=201)
def ingest_product_event(payload: ProductEventCreate, db: Session = Depends(get_db)):
    item = ProductEvent(
        event_name=payload.event_name,
        workspace_id=payload.workspace_id,
        actor_id=payload.actor_id,
        event_properties=payload.properties,
        is_synthetic=False,
        occurred_at=payload.occurred_at or datetime.now(timezone.utc),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "event_name": item.event_name,
        "workspace_id": item.workspace_id,
        "is_synthetic": item.is_synthetic,
        "occurred_at": item.occurred_at,
    }


def rice_score(item: Opportunity) -> float:
    """RICE = Reach × Impact × Confidence ÷ Effort."""
    return round((item.reach * item.impact * item.confidence) / max(item.effort, 0.1), 2)


def opportunity_payload(item: Opportunity) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "problem_statement": item.problem_statement,
        "theme": item.theme,
        "reach": item.reach,
        "impact": item.impact,
        "confidence": item.confidence,
        "effort": item.effort,
        "status": item.status,
        "rice_score": rice_score(item),
        "created_at": item.created_at,
    }


@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    feedback = list(db.scalars(select(Feedback)))
    opportunities = list(db.scalars(select(Opportunity)))
    experiments = list(db.scalars(select(Experiment)))
    theme_counts = Counter(item.theme for item in feedback)
    sentiment_counts = Counter(item.sentiment for item in feedback)
    theme_rows = [
        {"theme": theme, "count": count,
         "negative_count": sum(1 for item in feedback if item.theme == theme and item.sentiment == "negative")}
        for theme, count in theme_counts.most_common()
    ]
    for row in theme_rows:
        row["negative_share"] = round(row["negative_count"] / row["count"], 2) if row["count"] else 0
    recent = sorted(feedback, key=lambda item: item.created_at, reverse=True)[:5]
    return {
        "feedback_count": len(feedback),
        "negative_feedback": sentiment_counts.get("negative", 0),
        "opportunity_count": len(opportunities),
        "active_experiments": sum(1 for item in experiments if item.status == "Running"),
        "sentiment": dict(sentiment_counts),
        "themes": theme_rows,
        "top_opportunities": [opportunity_payload(item) for item in sorted(opportunities, key=rice_score, reverse=True)[:3]],
        "recent_feedback": [
            {"id": item.id, "text": item.text, "source": item.source, "segment": item.segment,
             "theme": item.theme, "sentiment": item.sentiment, "created_at": item.created_at}
            for item in recent
        ],
        "data_note": "Sample workspace seeded with synthetic feedback. Counts are illustrative, not customer evidence.",
    }


@app.get("/api/feedback")
def list_feedback(
    theme: str | None = None,
    sentiment: str | None = None,
    search: str | None = Query(default=None, max_length=200),
    db: Session = Depends(get_db),
):
    query = select(Feedback).order_by(desc(Feedback.created_at))
    if theme:
        query = query.where(Feedback.theme == theme)
    if sentiment:
        query = query.where(Feedback.sentiment == sentiment)
    if search:
        query = query.where(Feedback.text.ilike(f"%{search}%"))
    return list(db.scalars(query))


@app.post("/api/feedback", response_model=FeedbackOut, status_code=201)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    result = analyze_feedback(payload.text)
    item = Feedback(
        text=payload.text.strip(),
        source=payload.source,
        segment=payload.segment,
        theme=result["theme"],
        sentiment=result["sentiment"],
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    record_product_event(db, "feedback_created", {"feedback_id": item.id, "theme": item.theme, "source": item.source})
    return item


@app.get("/api/feedback/{feedback_id}/analysis")
def feedback_analysis(feedback_id: int, db: Session = Depends(get_db)):
    item = db.get(Feedback, feedback_id)
    if not item:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"feedback_id": item.id, **analyze_feedback(item.text)}


@app.get("/api/insights")
def insights(db: Session = Depends(get_db)):
    feedback = list(db.scalars(select(Feedback)))
    grouped = {}
    for item in feedback:
        grouped.setdefault(item.theme, []).append(item)
    results = []
    for theme, items in grouped.items():
        negative = sum(1 for item in items if item.sentiment == "negative")
        results.append({
            "theme": theme,
            "volume": len(items),
            "negative_count": negative,
            "negative_share": round(negative / len(items), 2),
            "signal": "Investigate" if negative / len(items) >= 0.5 else "Monitor",
            "evidence": [item.text for item in items[:3]],
        })
    return sorted(results, key=lambda row: (row["negative_share"], row["volume"]), reverse=True)


@app.get("/api/opportunities")
def list_opportunities(db: Session = Depends(get_db)):
    items = list(db.scalars(select(Opportunity)))
    return sorted((opportunity_payload(item) for item in items), key=lambda row: row["rice_score"], reverse=True)


@app.post("/api/opportunities", status_code=201)
def create_opportunity(payload: OpportunityCreate, db: Session = Depends(get_db)):
    item = Opportunity(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    record_product_event(db, "opportunity_created", {"opportunity_id": item.id, "theme": item.theme})
    return opportunity_payload(item)


@app.patch("/api/opportunities/{opportunity_id}/status")
def update_opportunity_status(
    opportunity_id: int, payload: OpportunityStatusUpdate, db: Session = Depends(get_db)
):
    allowed = {"Candidate", "Planned", "In progress", "Shipped", "Dropped"}
    if payload.status not in allowed:
        raise HTTPException(status_code=422, detail=f"Status must be one of: {', '.join(sorted(allowed))}")
    item = db.get(Opportunity, opportunity_id)
    if not item:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    previous_status = item.status
    item.status = payload.status
    db.commit()
    db.refresh(item)
    if previous_status != payload.status and payload.status in {"Planned", "In progress"}:
        record_product_event(db, "opportunity_prioritized", {"opportunity_id": item.id, "status": item.status})
    return opportunity_payload(item)


@app.get("/api/experiments")
def list_experiments(db: Session = Depends(get_db)):
    items = list(db.scalars(select(Experiment).order_by(desc(Experiment.created_at))))
    return [
        {"id": item.id, "title": item.title, "hypothesis": item.hypothesis,
         "success_metric": item.success_metric, "baseline_value": item.baseline_value,
         "target_value": item.target_value, "status": item.status, "owner": item.owner,
         "created_at": item.created_at}
        for item in items
    ]


@app.post("/api/experiments", status_code=201)
def create_experiment(payload: ExperimentCreate, db: Session = Depends(get_db)):
    item = Experiment(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    record_product_event(db, "experiment_created", {"experiment_id": item.id})
    return {"id": item.id, **payload.model_dump(), "created_at": item.created_at}


@app.patch("/api/experiments/{experiment_id}/status")
def update_experiment_status(
    experiment_id: int, payload: ExperimentStatusUpdate, db: Session = Depends(get_db)
):
    allowed = {"Planned", "Running", "Completed", "Paused"}
    if payload.status not in allowed:
        raise HTTPException(status_code=422, detail=f"Status must be one of: {', '.join(sorted(allowed))}")
    item = db.get(Experiment, experiment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Experiment not found")
    previous_status = item.status
    item.status = payload.status
    db.commit()
    db.refresh(item)
    if previous_status != payload.status and payload.status == "Completed":
        record_product_event(db, "experiment_completed", {"experiment_id": item.id})
    return {"id": item.id, "title": item.title, "status": item.status}


@app.post("/api/demo/reseed")
def reseed_demo_data(db: Session = Depends(get_db)):
    """Reset the demo workspace to its original synthetic sample dataset."""
    db.query(Feedback).delete()
    db.query(Opportunity).delete()
    db.query(Experiment).delete()
    db.query(ProductEvent).delete()
    db.commit()
    seed_demo_data(db)
    seed_product_events(db)
    return {"status": "reseeded", "message": "Synthetic demo data restored."}
