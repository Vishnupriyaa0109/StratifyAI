# Technical architecture

## System context

```text
Product team member
       |
       v
React + TypeScript + Vite
       |  HTTP / JSON
       v
FastAPI application
       |
       +--> Baseline feedback analysis
       |
       v
SQLAlchemy models / sessions
       |
       v
SQLite (local demo) or PostgreSQL
```

## Frontend
- React single-page app with four workflow views: Overview, Feedback, Opportunities, Experiments.
- Typed API client is isolated in `frontend/src/api.ts`.
- API origin can be set with `VITE_API_URL`; default is `http://localhost:8000`.
- UI presents source records and calls the backend for persistence and aggregate data.

## Backend
- FastAPI owns API routing and input validation.
- Pydantic schemas validate incoming payloads.
- SQLAlchemy models represent feedback, opportunities, and experiments.
- `analysis.py` contains a deliberately simple, deterministic keyword baseline.
- `seed.py` creates a small synthetic workspace for first-run exploration.

## Data model
### Feedback
`id, source, segment, text, theme, sentiment, created_at`

### Opportunity
`id, title, problem_statement, theme, reach, impact, confidence, effort, status, created_at`

### Experiment
`id, title, hypothesis, success_metric, baseline_value, target_value, status, owner, created_at`

## API conventions
- JSON requests and responses.
- Standard HTTP status codes and FastAPI validation errors.
- RICE is calculated on the server from persisted input values.
- Demo reset is destructive and should not be enabled without protection in a real deployment.

## Configuration
- `DATABASE_URL`: SQLAlchemy database URL; defaults to local SQLite.
- `FRONTEND_ORIGIN`: comma-separated allowed CORS origins.
- `VITE_API_URL`: frontend API base URL.

## Known technical limitations
- No authentication or workspace tenant boundary. Do not deploy for private customer data as-is.
- No migrations yet; SQLAlchemy creates tables at startup. Add Alembic before evolving a production schema.
- No pagination; current list endpoints target a small MVP dataset.
- Keyword classification is language- and wording-sensitive and cannot reliably infer intent, negation, sarcasm, or multiple themes.
- No background ingestion or model-serving infrastructure.
- No server-side event analytics or audit log.

## Next architecture increments
1. Add Alembic migrations and versioned API contracts.
2. Add user/workspace identity and enforce authorisation at every data query.
3. Add pagination, filtering indexes, and import idempotency.
4. Add classifier evaluation dataset, reviewer corrections, and model monitoring before replacing the baseline.
5. Add async ingestion only when source connectors create a demonstrated need.
