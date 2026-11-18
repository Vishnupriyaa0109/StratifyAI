# StratifyAI
### From Customer Voices to Confident Product Decisions.

**StratifyAI** is an AI-assisted Product Decision Intelligence workspace by **Vaeshaa**. It helps product teams turn unstructured customer feedback into reviewable themes, prioritised opportunities, and measurable experiments.

> **Portfolio MVP notice:** This repository is a working demonstration built with synthetic sample feedback. The classifier is a transparent keyword baseline, not a trained AI model. Demo RICE inputs and experiment baselines/targets are illustrative assumptions, not verified customer research or business results.

<p align="center">
  <b>Feedback → Insights → Opportunities → Experiments → Learning</b>
</p>

## Product problem

Product teams receive customer signals from support conversations, app feedback, surveys, reviews, and interviews. Those signals are often fragmented. It becomes difficult to answer:

- Which customer problems are recurring?
- Which segments are affected?
- What should the team prioritise, and why?
- What hypothesis should be tested?
- Which metric would tell us whether a change helped?

StratifyAI brings these steps into one inspectable workflow, keeping the link between customer evidence and product decisions visible.

## What is implemented

| Area | Current MVP capability |
|---|---|
| Feedback inbox | Add feedback with source and segment; search; view theme and sentiment suggestions |
| Insight engine | Keyword-based theme and sentiment classification with a transparent method label |
| Dashboard | Feedback volume, sentiment distribution, themes, recent feedback, and top RICE opportunities |
| Opportunity backlog | Create customer problem statements, calculate RICE, and update status |
| Experiment tracker | Create hypotheses, define success metrics and optional baseline/target values, update status |
| Demo workspace | Seeded synthetic examples and a reset-to-demo action |
| API | FastAPI endpoints with SQLAlchemy persistence |
| Frontend | Responsive React + TypeScript + Vite application |

### What is not claimed as implemented

- No production-trained machine-learning model or validated model-accuracy score.
- No live integrations with external customer-feedback platforms.
- No authentication, role-based access control, or multi-tenant isolation yet.
- No causal inference, A/B test execution, statistical significance calculation, or automated experiment readout.
- No real customer interviews or measured business impact are represented by the seeded records.

These are deliberate next steps, not hidden capabilities.

## Product workflow

1. **Capture** — add customer feedback, including its source and segment.
2. **Organise** — receive a suggested theme and sentiment with a simple explanation.
3. **Inspect** — review theme volume and negative-signal concentration; return to the original feedback before acting.
4. **Prioritise** — convert a problem into an opportunity and compare it using RICE.
5. **Experiment** — record a falsifiable hypothesis, a success metric, and optional baseline/target values.
6. **Learn** — update experiment status and use the result to inform the next product decision. The MVP tracks workflow state; it does not claim to measure causal impact.

## Architecture

```text
StratifyAI/
├── frontend/
│   ├── index.html
│   └── src/
│       ├── App.tsx          # Dashboard and product workflows
│       ├── api.ts           # Typed API client
│       ├── main.tsx
│       ├── styles.css
│       └── types.ts
├── backend/
│   ├── app/
│   │   ├── analysis.py      # Explainable keyword baseline
│   │   ├── database.py      # SQLAlchemy engine/session
│   │   ├── main.py          # FastAPI routes
│   │   ├── models.py        # Feedback/opportunity/experiment models
│   │   ├── schemas.py       # Request validation
│   │   └── seed.py          # Synthetic demo dataset
│   ├── tests/
│   │   └── test_analysis.py
│   ├── requirements.txt
│   └── .env.example
├── docs/
└── README.md
```

**Frontend:** React 18, TypeScript, Vite, Lucide icons  
**Backend:** Python, FastAPI, Pydantic, SQLAlchemy  
**Database:** SQLite for quick local development; PostgreSQL supported through `DATABASE_URL`

## Run locally

### Requirements

- Python 3.10+
- Node.js 20+
- npm

### 1. Start the API

From the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start FastAPI:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default, the API uses a local SQLite database file at `backend/stratifyai.db`. The first startup creates the tables and seeds synthetic demo data when the feedback table is empty.

- API root: http://localhost:8000
- Health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs

### 2. Start the frontend

In a second terminal, from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

The frontend expects the API at `http://localhost:8000` by default. To point it elsewhere, create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

For a non-default frontend origin, configure `FRONTEND_ORIGIN` in the backend environment. Comma-separated origins are supported.

### 3. Optional: use PostgreSQL

Create a database, then set the backend `DATABASE_URL` environment variable. Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/stratifyai
FRONTEND_ORIGIN=http://localhost:5173
```

The Postgres driver is included in `backend/requirements.txt`. SQLite is the default so the MVP can be run without Docker.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/dashboard` | Dashboard aggregates and recent signals |
| GET | `/api/feedback` | List/search/filter feedback |
| POST | `/api/feedback` | Add feedback and classify it |
| GET | `/api/feedback/{id}/analysis` | Inspect classification and explanation |
| GET | `/api/insights` | Theme-level volume and negative share |
| GET | `/api/opportunities` | List opportunities ordered by RICE |
| POST | `/api/opportunities` | Create an opportunity |
| PATCH | `/api/opportunities/{id}/status` | Update opportunity status |
| GET | `/api/experiments` | List experiments |
| POST | `/api/experiments` | Create an experiment |
| PATCH | `/api/experiments/{id}/status` | Update experiment status |
| POST | `/api/demo/reseed` | Reset the workspace to synthetic sample data |

See the interactive OpenAPI documentation at `/docs` after starting the backend.

## Product methodology

### Feedback classification

The MVP uses an intentionally interpretable keyword baseline:

- Theme groups: Onboarding, Reliability, Pricing, Workflow, Reporting, and Other.
- Sentiment groups: positive, neutral, and negative.
- A small set of matched terms determines the label.
- Unmatched records are placed in Other for human review.

This is a starting point for product exploration, not a substitute for contextual qualitative analysis. Negation, sarcasm, domain context, multilingual input, and overlapping themes can cause errors. Human review is expected.

### RICE prioritisation

The opportunity backlog calculates:

`RICE = (Reach × Impact × Confidence) ÷ Effort`

- **Reach:** estimated users/customers affected in a defined period.
- **Impact:** relative impact using a consistent team scale.
- **Confidence:** confidence in the reach and impact estimates.
- **Effort:** estimated person-time required.

The application calculates the score from entered values. Teams should document their scoring assumptions and use the result as a discussion aid, not an automatic roadmap decision.

### Experiment design

Each experiment stores a hypothesis, success metric, optional baseline and target, owner, and status. Before a real experiment, define eligible users, sample size, duration, guardrail metrics, analysis method, and decision threshold. The current tracker does not run experiments or infer causality.

## Quality checks

Run the backend classifier tests:

```bash
cd backend
pip install -r requirements.txt
pytest
```

Build the frontend:

```bash
cd frontend
npm install
npm run build
```

## Product roadmap

| Priority | Next increment | Why it matters |
|---|---|---|
| P0 | Automated frontend/backend test coverage and CI | Protect core workflows from regressions |
| P0 | Authentication and workspace-level authorisation | Make the app safe for real team data |
| P1 | CSV import with validation and duplicate handling | Reduce manual feedback entry |
| P1 | Human-in-the-loop theme editing and audit trail | Improve trust and classification quality |
| P1 | Evidence links from insights to opportunities | Preserve traceability through prioritisation |
| P2 | Embedding-assisted clustering and topic discovery | Surface themes beyond hand-authored keywords |
| P2 | Experiment results, guardrails, and decision log | Close the learning loop |
| P2 | Source connectors and scheduled ingestion | Reduce fragmented feedback operations |

## Product success measures to validate

These are proposed measures, not measured outcomes:

- **Activation:** percentage of new workspaces that add feedback and create their first opportunity.
- **Time to first insight:** time from first feedback import to a reviewed insight.
- **Insight review rate:** percentage of suggested themes accepted or edited by a human.
- **Decision traceability:** percentage of prioritised opportunities linked to supporting feedback.
- **Experiment follow-through:** percentage of planned experiments that reach a documented decision.
- **Workflow retention:** teams returning to review feedback and update opportunities over time.

Each metric needs a precise event definition, denominator, cohort, and measurement window before being used in a real product review.

## Security and data handling

Do not upload confidential, personal, or customer-identifiable data to this demo deployment. Before production use, add authentication, authorisation, rate limiting, secrets management, retention/deletion controls, input sanitisation appropriate to the product, operational logging, backups, and a privacy/security review.

## Contributing

Issues and pull requests are welcome. For substantial changes, describe the user problem, proposed behaviour, alternatives considered, and how the change will be tested.

## About

**Vaeshaa · StratifyAI**  
*From Customer Voices to Confident Product Decisions.*

Built as a product-management and full-stack engineering portfolio project.
