import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.analysis import analyze_feedback


def test_reliability_feedback_is_classified():
    result = analyze_feedback("The dashboard crashes and loading is slow.")
    assert result["theme"] == "Reliability"
    assert result["sentiment"] == "negative"
    assert result["method"] == "keyword baseline v1"


def test_positive_feedback_is_positive():
    result = analyze_feedback("The setup was easy and the tutorial was helpful.")
    assert result["theme"] == "Onboarding"
    assert result["sentiment"] == "positive"


def test_unmatched_feedback_is_kept_for_review():
    result = analyze_feedback("Could you add support for my unusual use case?")
    assert result["theme"] == "Other"
    assert result["confidence"] == 0.35


def test_sentiment_tokenisation_handles_punctuation_and_word_forms():
    result = analyze_feedback("The dashboard crashes, and loading is slow.")
    assert result["sentiment"] == "negative"


def test_rice_score_calculates_reach_impact_confidence_over_effort():
    from types import SimpleNamespace
    from app.main import rice_score

    opportunity = SimpleNamespace(reach=80, impact=2.5, confidence=0.8, effort=3)
    assert rice_score(opportunity) == 53.33


from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from app.analytics import compute_product_metrics


def test_activation_funnel_uses_distinct_workspaces_and_calculates_rates():
    now = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
    events = [
        SimpleNamespace(event_name="workspace_created", workspace_id="w1", occurred_at=now - timedelta(days=20), is_synthetic=True),
        SimpleNamespace(event_name="feedback_created", workspace_id="w1", occurred_at=now - timedelta(days=19), is_synthetic=True),
        SimpleNamespace(event_name="insight_reviewed", workspace_id="w1", occurred_at=now - timedelta(days=18), is_synthetic=True),
        SimpleNamespace(event_name="opportunity_created", workspace_id="w1", occurred_at=now - timedelta(days=17), is_synthetic=True),
        SimpleNamespace(event_name="workspace_created", workspace_id="w2", occurred_at=now - timedelta(days=9), is_synthetic=True),
        SimpleNamespace(event_name="feedback_created", workspace_id="w2", occurred_at=now - timedelta(days=8), is_synthetic=True),
        SimpleNamespace(event_name="workspace_active", workspace_id="w2", occurred_at=now - timedelta(days=1), is_synthetic=True),
        # Duplicate event must not increase the number of converted workspaces.
        SimpleNamespace(event_name="feedback_created", workspace_id="w1", occurred_at=now - timedelta(days=18), is_synthetic=True),
    ]

    result = compute_product_metrics(events, now=now)
    assert result["cohort_workspaces"] == 2
    assert result["funnel"][1]["workspaces"] == 2
    assert result["funnel"][2]["workspaces"] == 1
    assert result["activation_rate"] == 50.0
    assert result["weekly_active_workspaces"] == 1
    assert result["north_star_workspaces"] == 1


def test_d7_retention_uses_only_matured_signup_cohorts():
    now = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
    events = [
        SimpleNamespace(event_name="workspace_created", workspace_id="retained", occurred_at=now - timedelta(days=20), is_synthetic=True),
        SimpleNamespace(event_name="workspace_active", workspace_id="retained", occurred_at=now - timedelta(days=11), is_synthetic=True),
        SimpleNamespace(event_name="workspace_created", workspace_id="churned", occurred_at=now - timedelta(days=20), is_synthetic=True),
        SimpleNamespace(event_name="workspace_created", workspace_id="too_new", occurred_at=now - timedelta(days=9), is_synthetic=True),
    ]

    result = compute_product_metrics(events, now=now)
    assert result["d7_retention"]["eligible_workspaces"] == 2
    assert result["d7_retention"]["retained_workspaces"] == 1
    assert result["d7_retention"]["rate"] == 50.0


def test_metric_output_labels_synthetic_data():
    now = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
    events = [
        SimpleNamespace(event_name="workspace_created", workspace_id="demo", occurred_at=now - timedelta(days=2), is_synthetic=True),
        SimpleNamespace(event_name="workspace_active", workspace_id="demo", occurred_at=now - timedelta(days=1), is_synthetic=False),
    ]
    result = compute_product_metrics(events, now=now)
    assert result["event_quality"]["synthetic_events"] == 1
    assert result["event_quality"]["observed_events"] == 1
    assert "synthetic" in result["data_note"].lower()


def test_product_event_schema_rejects_unknown_event_names():
    import pytest
    from pydantic import ValidationError
    from app.schemas import ProductEventCreate

    with pytest.raises(ValidationError):
        ProductEventCreate(event_name="random_event", workspace_id="workspace-1")

    valid = ProductEventCreate(
        event_name="insight_reviewed",
        workspace_id="workspace-1",
        properties={"review_outcome": "accepted"},
    )
    assert valid.event_name == "insight_reviewed"
