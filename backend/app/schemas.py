from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    text: str = Field(min_length=8, max_length=4000)
    source: str = Field(default="In-app", max_length=80)
    segment: str = Field(default="Unknown", max_length=100)


class FeedbackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: str
    source: str
    segment: str
    theme: str
    sentiment: str
    created_at: datetime


class OpportunityCreate(BaseModel):
    title: str = Field(min_length=4, max_length=180)
    problem_statement: str = Field(min_length=8, max_length=3000)
    theme: str = "Other"
    reach: float = Field(default=1, ge=1, le=100)
    impact: float = Field(default=2, ge=0.25, le=3)
    confidence: float = Field(default=0.7, ge=0.1, le=1)
    effort: float = Field(default=2, ge=0.5, le=100)
    status: str = "Candidate"


class OpportunityOut(BaseModel):
    id: int
    title: str
    problem_statement: str
    theme: str
    reach: float
    impact: float
    confidence: float
    effort: float
    status: str
    rice_score: float
    created_at: datetime


class ExperimentCreate(BaseModel):
    title: str = Field(min_length=4, max_length=180)
    hypothesis: str = Field(min_length=8, max_length=3000)
    success_metric: str = Field(min_length=2, max_length=180)
    baseline_value: float | None = None
    target_value: float | None = None
    owner: str = "Product"
    status: str = "Planned"


class ExperimentStatusUpdate(BaseModel):
    status: str


class OpportunityStatusUpdate(BaseModel):
    status: str


ALLOWED_PRODUCT_EVENTS = {
    "workspace_created",
    "feedback_created",
    "insight_reviewed",
    "opportunity_created",
    "opportunity_prioritized",
    "experiment_created",
    "experiment_completed",
    "workspace_active",
}


class ProductEventCreate(BaseModel):
    event_name: str = Field(min_length=3, max_length=80)
    workspace_id: str = Field(min_length=2, max_length=100)
    actor_id: str | None = Field(default=None, max_length=100)
    properties: dict = Field(default_factory=dict)
    occurred_at: datetime | None = None

    @classmethod
    def validate_event_name(cls, value: str) -> str:
        if value not in ALLOWED_PRODUCT_EVENTS:
            raise ValueError(f"Unsupported event. Choose one of: {', '.join(sorted(ALLOWED_PRODUCT_EVENTS))}")
        return value
