# Product requirements document — StratifyAI MVP

**Status:** MVP specification / living document  
**Version:** 0.1  
**Owner:** Product  
**Audience:** Product, design, engineering

## 1. Context
Product teams receive feedback from multiple customer touchpoints. StratifyAI creates a lightweight place to capture signals, inspect suggested themes, prioritise problems, and record experiments.

## 2. Goals
- Reduce the effort required to make feedback reviewable.
- Preserve original customer wording alongside suggested classifications.
- Make opportunity prioritisation explicit and comparable.
- Encourage testable hypotheses and measurable success criteria.
- Demonstrate an end-to-end product workflow in a portfolio-ready MVP.

## 3. Non-goals
- Replacing a CRM, support desk, data warehouse, or product analytics platform.
- Making autonomous roadmap decisions.
- Claiming statistical significance or causal impact.
- Production-grade multi-tenant security in the current demo.
- Training a custom LLM or supervised classifier in the current MVP.

## 4. User stories and acceptance criteria

### F-01 — Capture feedback
As a product team member, I can add a feedback record with text, source, and segment.
- Text is required and validated for minimum/maximum length.
- The original text is retained.
- The service returns the created record and suggested theme/sentiment.
- Empty or invalid payloads return a validation error.

### F-02 — Inspect feedback
As a product manager, I can browse and search feedback.
- Records display original text, theme, sentiment, source, segment, and creation date.
- Search matches text, theme, source, or segment.
- Empty search results are explained rather than silently hidden.

### F-03 — Explain classification
As a reviewer, I can see the classification method and a short explanation.
- Every prediction indicates the baseline method.
- Unmatched records are assigned to Other for human review.
- The UI communicates that labels are heuristic suggestions.

### F-04 — View aggregate insights
As a product manager, I can inspect feedback volume by theme and sentiment.
- Dashboard totals are derived from stored feedback.
- Theme volume and negative share can be compared.
- The dashboard labels the seeded workspace as synthetic/demo data.

### O-01 — Create and prioritise opportunities
As a product manager, I can record a problem statement and score reach, impact, confidence, and effort.
- All numeric inputs are validated against documented ranges.
- RICE is calculated as Reach × Impact × Confidence ÷ Effort.
- Opportunities are ordered by score, highest first.
- Users can change status; scores remain inspectable.

### E-01 — Track experiments
As a product manager, I can capture a hypothesis and success metric.
- Title, hypothesis, and metric are required.
- Baseline and target are optional numeric inputs.
- Status can move among Planned, Running, Completed, and Paused.
- The UI makes clear that tracking status is not experiment execution or statistical analysis.

### D-01 — Reset demo dataset
As a demo user, I can restore the seeded sample workspace.
- The action requires confirmation.
- Existing records in this demo database are deleted and synthetic seed records restored.
- The action is labelled as destructive.

## 5. Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Create and list feedback | Must |
| FR-02 | Search feedback | Must |
| FR-03 | Apply transparent baseline theme/sentiment suggestions | Must |
| FR-04 | Aggregate dashboard counts | Must |
| FR-05 | Create, list, score, and update opportunities | Must |
| FR-06 | Create, list, and update experiments | Must |
| FR-07 | Seed and reset sample data | Should |
| FR-08 | Export filtered feedback | Later |
| FR-09 | Edit or override classifications with audit trail | Later |
| FR-10 | External feedback connectors | Later |

## 6. Non-functional requirements
- **Usability:** core workflows should be understandable without training.
- **Performance:** for a small demo dataset, standard list and dashboard calls should feel responsive.
- **Reliability:** invalid input should return actionable HTTP errors.
- **Maintainability:** frontend calls are centralised; backend domain logic is separated from route handlers.
- **Security:** demo is not approved for real sensitive/customer data; production auth, access control, secrets handling, and retention controls are prerequisites.
- **Accessibility:** labels, keyboard-operable controls, meaningful status text, and responsive layout should be maintained.

## 7. MVP instrumentation proposal
Capture events in a future analytics implementation: feedback_created, feedback_search_used, classification_reviewed, opportunity_created, opportunity_status_changed, experiment_created, experiment_status_changed. Define identity, workspace, timestamp, and event properties before shipping instrumentation.

## 8. Release acceptance checklist
- [ ] Backend starts and health endpoint responds.
- [ ] Database initialises on first run.
- [ ] Synthetic data appears in dashboard.
- [ ] Feedback can be created and searched.
- [ ] Opportunity score is calculated correctly.
- [ ] Opportunity status can be updated.
- [ ] Experiments can be created and statuses updated.
- [ ] UI clearly labels synthetic data and heuristic classification.
- [ ] Frontend production build succeeds.
- [ ] Automated tests and CI pass.
