# Product Analytics & Business Metrics Specification

**Status:** Implemented MVP instrumentation and illustrative metrics  
**Scope:** Activation, engagement, retention, conversion funnel, and time to first value  
**Data warning:** Seeded analytics events are synthetic and are only for demonstrating metric calculation. They are not actual customer, revenue, or business performance.

## 1. Measurement philosophy

A product metric is only useful when its event definition, population, time window, and exclusions are explicit. StratifyAI stores a small append-only event stream and calculates distinct-workspace metrics from it.

The demo intentionally distinguishes:
- **Synthetic events:** seeded records used to make the dashboard explorable.
- **Observed events:** events captured through the running application or event-ingestion API.

The metrics API reports both counts and a synthetic share. Do not combine the displayed numbers with claims about real users or commercial performance.

## 2. Event taxonomy

| Event | Trigger | Required properties / context |
|---|---|---|
| `workspace_created` | Workspace is created | `workspace_id`, `occurred_at` |
| `feedback_created` | Feedback record is saved | Optional source and theme |
| `insight_reviewed` | A person reviews a suggested insight | Optional review outcome |
| `opportunity_created` | A customer problem is added to the backlog | Optional theme |
| `opportunity_prioritized` | Opportunity moves to Planned or In progress | Optional status |
| `experiment_created` | Experiment plan is created | Optional experiment type |
| `experiment_completed` | Experiment status moves to Completed | Optional experiment ID |
| `workspace_active` | Meaningful workspace action | Optional product surface |

Events are scoped by `workspace_id`. `actor_id` is optional. The demo avoids collecting personal identifiers. Do not place names, email addresses, customer message text, or secrets in event properties.

### Ingestion contract

- `POST /api/events` accepts a whitelisted event name, workspace ID, optional actor ID, optional JSON properties, and optional event timestamp.
- Events are stored with a synthetic/observed provenance flag.
- Unknown event names are rejected by request validation.
- In the demo there is no authentication or tenant isolation; do not expose this ingestion endpoint to untrusted traffic with real data.

Core actions in the app also emit observed events: feedback creation, opportunity creation, opportunity promotion, experiment creation, and experiment completion.

## 3. Metric definitions

| Metric | Formula | Window / population | Interpretation |
|---|---|---|---|
| Activation rate | Unique workspaces with `insight_reviewed` ÷ unique workspaces with `workspace_created` × 100 | Signup events in trailing 30 days | Proxy for reaching the first human-reviewed insight |
| Feedback capture conversion | Unique workspaces with `feedback_created` ÷ signup workspaces × 100 | Same signup cohort | Early onboarding step completion |
| Opportunity conversion | Unique workspaces with `opportunity_created` ÷ signup workspaces × 100 | Same signup cohort | Evidence translated into a problem statement |
| Weekly active workspaces | Distinct workspaces with a meaningful non-signup event | Trailing 7 days | Directional workspace engagement |
| D7 retention | Workspaces active during days 7–14 ÷ eligible signup workspaces × 100 | Signup cohorts at least 14 days old | Return behaviour after first-week onboarding |
| Time to first insight | Median time from signup to first `insight_reviewed` | Activated workspaces in trailing 30-day signup cohort | Time to first value |
| Evidence-linked decision proxy | Unique workspaces with both `insight_reviewed` and `opportunity_created` | Same 30-day signup cohort | North-star proxy for insight-to-decision flow |

### Funnel logic
The funnel is based on distinct workspaces, not raw event counts. A workspace with five feedback events only contributes once to the feedback-captured stage. Each stage reports conversion from the preceding stage and from signup.

### D7 cohort maturity
A workspace is eligible for D7 retention only after at least 14 days have elapsed since signup. It is counted as retained when a meaningful event falls in the interval [signup + 7 days, signup + 14 days). This avoids counting newly acquired workspaces as churned before they have had time to return.

## 4. Proposed north-star metric

**Reviewed customer problems that lead to a documented product decision per active workspace per month.**

This is a product-value hypothesis, not a validated metric. The current application reports a simpler proxy: workspaces that have both an `insight_reviewed` and an `opportunity_created` event in the cohort window. A future version should link individual feedback, opportunities, decisions, and experiment readouts by durable IDs before calling the metric a fully traceable decision outcome.

## 5. Instrumentation QA and data quality

Before trusting a metric:
1. Validate each event fires once at the intended user action.
2. Check the correct workspace identifier is attached.
3. Confirm event timestamps use UTC and describe occurrence time, not ingestion time.
4. Exclude test/demo traffic from production reporting.
5. Deduplicate client retries with an idempotency key in a production version.
6. Audit event properties for personal or sensitive data.
7. Compare raw event counts with product database records.
8. Check for impossible event orderings and missing funnel context.

The MVP's `is_synthetic` field makes sample provenance inspectable. It does not replace a production data-quality pipeline.

## 6. How to inspect the implementation

- `backend/app/models.py` — append-only `ProductEvent` data model.
- `backend/app/analytics.py` — metric calculations and cohort maturity logic.
- `backend/app/seed.py` — deterministic synthetic event generator.
- `backend/app/main.py` — event ingestion and metrics endpoints; core workflow instrumentation.
- `backend/tests/test_analysis.py` — funnel, distinct-workspace, D7 retention, provenance, and RICE tests.
- `frontend/src/App.tsx` — Metrics dashboard.
- `frontend/src/api.ts` and `frontend/src/types.ts` — typed API integration.

## 7. Business decisions these metrics could inform

| Signal | Possible product question | Follow-up analysis |
|---|---|---|
| Low feedback capture conversion | Is onboarding asking for too much before value is visible? | Interview drop-offs; inspect setup steps |
| Feedback high, insight review low | Are suggestions low quality or hard to review? | Label audit; reviewer usability sessions |
| Insight review high, opportunity conversion low | Are insights not actionable or is prioritisation a separate workflow? | Observe roadmap review; inspect problem framing |
| Activation healthy, D7 low | Is first value not sustained? | Retention cohorts and recurring use cases |
| Long time to first insight | Which step adds the most delay? | Time-between-events distribution |
| High synthetic share | Are current dashboard values still mainly demo data? | Verify event provenance and data source |

Metrics are diagnostic signals, not proof of causality. Segment analysis, qualitative research, and controlled experiments are needed before committing to interventions.

## 8. Next increments

- Add actor/workspace authentication and authorisation.
- Add event idempotency keys and server-side event schema versions.
- Add pagination and a retention-policy-aware event store.
- Add a reviewed-feedback action in the UI and a persistent review history.
- Add cohort trend charts and configurable time windows.
- Add event-level audit tools and anomaly checks.
- Separate production, staging, and synthetic demo environments.
