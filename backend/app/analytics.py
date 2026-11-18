"""Business and product metric calculations over the product event stream.

All rates are calculated from distinct workspaces to avoid counting repeated events
as additional conversions. Times are normalised to UTC to support SQLite/PostgreSQL.
"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from statistics import median
from typing import Iterable


FUNNEL_STAGES = [
    ("workspace_created", "Workspace created"),
    ("feedback_created", "Feedback captured"),
    ("insight_reviewed", "Insight reviewed"),
    ("opportunity_created", "Opportunity created"),
    ("experiment_created", "Experiment created"),
]


def as_utc(value: datetime) -> datetime:
    """Treat naive database datetimes as UTC and normalise aware values."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def compute_product_metrics(events: Iterable, now: datetime | None = None) -> dict:
    now = as_utc(now or datetime.now(timezone.utc))
    all_events = list(events)
    normalized = [
        {
            "name": event.event_name,
            "workspace": event.workspace_id,
            "at": as_utc(event.occurred_at),
            "synthetic": bool(getattr(event, "is_synthetic", False)),
        }
        for event in all_events
    ]

    start_30d = now - timedelta(days=30)
    start_7d = now - timedelta(days=7)
    signups = {
        row["workspace"]: row["at"]
        for row in normalized
        if row["name"] == "workspace_created" and start_30d <= row["at"] <= now
    }

    by_workspace = defaultdict(list)
    for row in normalized:
        if row["workspace"] in signups:
            signup_at = signups[row["workspace"]]
            if signup_at <= row["at"] < signup_at + timedelta(days=30):
                by_workspace[row["workspace"]].append(row)

    funnel = []
    previous_count = None
    cohort_size = len(signups)
    for event_name, label in FUNNEL_STAGES:
        converted = sum(
            1 for rows in by_workspace.values()
            if any(row["name"] == event_name for row in rows)
        )
        funnel.append({
            "stage": event_name,
            "label": label,
            "workspaces": converted,
            "conversion_from_previous": round(converted / previous_count * 100, 1)
                if previous_count else (100.0 if converted else 0.0),
            "conversion_from_signup": round(converted / cohort_size * 100, 1)
                if cohort_size else 0.0,
        })
        previous_count = converted

    active_workspaces = {
        row["workspace"] for row in normalized
        if row["at"] >= start_7d and row["at"] <= now and row["name"] != "workspace_created"
    }

    eligible_d7 = {
        workspace: signup_at for workspace, signup_at in signups.items()
        if now >= signup_at + timedelta(days=14)
    }
    retained_d7 = set()
    for workspace, signup_at in eligible_d7.items():
        lower = signup_at + timedelta(days=7)
        upper = signup_at + timedelta(days=14)
        if any(
            row["workspace"] == workspace and lower <= row["at"] < upper
            and row["name"] != "workspace_created"
            for row in normalized
        ):
            retained_d7.add(workspace)

    first_insight_minutes = []
    north_star_workspaces = 0
    for workspace, rows in by_workspace.items():
        signup_at = signups[workspace]
        insights = [
            row["at"] for row in rows
            if row["name"] == "insight_reviewed" and row["at"] >= signup_at
        ]
        if insights:
            first_insight_minutes.append((min(insights) - signup_at).total_seconds() / 60)
        has_insight = bool(insights)
        has_opportunity = any(row["name"] == "opportunity_created" for row in rows)
        if has_insight and has_opportunity:
            north_star_workspaces += 1

    synthetic_events = sum(1 for row in normalized if row["synthetic"])
    observed_events = len(normalized) - synthetic_events
    return {
        "window_days": 30,
        "cohort_workspaces": cohort_size,
        "weekly_active_workspaces": len(active_workspaces),
        "d7_retention": {
            "eligible_workspaces": len(eligible_d7),
            "retained_workspaces": len(retained_d7),
            "rate": round(len(retained_d7) / len(eligible_d7) * 100, 1)
                if eligible_d7 else None,
        },
        "activation_rate": funnel[2]["conversion_from_signup"] if cohort_size else 0.0,
        "north_star_workspaces": north_star_workspaces,
        "median_time_to_first_insight_minutes": round(median(first_insight_minutes), 1)
            if first_insight_minutes else None,
        "funnel": funnel,
        "event_quality": {
            "synthetic_events": synthetic_events,
            "observed_events": observed_events,
            "synthetic_share": round(synthetic_events / len(normalized) * 100, 1)
                if normalized else 0.0,
        },
        "data_note": (
            "Metrics are computed from synthetic sample events plus any events captured in this local demo. "
            "They are illustrative and must not be presented as actual customer or commercial performance."
        ),
    }
