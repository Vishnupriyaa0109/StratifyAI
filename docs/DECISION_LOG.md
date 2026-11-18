# Product and engineering decision log

This log records current implementation choices and their rationale. Decisions should be revised when new evidence changes the trade-off.

## D-001 — Build one traceable product workflow
**Decision:** Connect feedback, insight, opportunity prioritisation, and experiment tracking in one MVP.  
**Rationale:** A feedback dashboard alone does not demonstrate how insights affect product decisions.  
**Trade-off:** Broad workflow coverage means each stage is intentionally lightweight.

## D-002 — Use a transparent keyword baseline first
**Decision:** Implement deterministic keyword-based theme and sentiment suggestions.  
**Rationale:** The demo can explain every rule, run locally, and avoid implying model performance without evaluation data.  
**Trade-off:** Limited recall, precision, context understanding, and language coverage. Human review is required.

## D-003 — Use RICE as a decision aid
**Decision:** Calculate RICE from visible reach, impact, confidence, and effort fields.  
**Rationale:** Makes prioritisation assumptions inspectable and easy to discuss.  
**Trade-off:** The score is sensitive to inconsistent scales and subjective estimates; it is not an objective measure of value.

## D-004 — Use SQLite by default, support PostgreSQL
**Decision:** Configure SQLAlchemy via DATABASE_URL; default to SQLite for local onboarding.  
**Rationale:** Quick local setup without requiring a database container; PostgreSQL is supported for a more realistic deployment.  
**Trade-off:** Production schema management, migrations, backups, and operational hardening remain future work.

## D-005 — Seed synthetic records
**Decision:** Provide clearly labelled sample feedback and example opportunities/experiments.  
**Rationale:** A new reviewer can explore the workflows immediately.  
**Trade-off:** Synthetic records cannot validate user demand or business outcomes and must never be presented as real customer evidence.

## D-006 — Defer integrations, authentication, and experiment analytics
**Decision:** Keep connectors, multi-user security, and statistical experiment analysis out of the current demo.  
**Rationale:** Reduce setup complexity and focus on proving the core product workflow.  
**Trade-off:** The MVP is not suitable for production or sensitive customer data until these controls are designed and implemented.
