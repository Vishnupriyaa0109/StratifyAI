# User Stories and Acceptance Criteria

## Feedback

**US-01 — Capture a feedback signal**  
As a product manager, I want to add a feedback item with source and segment so that the team can review customer signals in one workspace.

Acceptance criteria:
- Feedback text is required and bounded.
- Source and segment are stored.
- Theme and sentiment suggestions are attached.
- Original customer wording remains visible.

**US-02 — Find relevant feedback**  
As a product manager, I want to search the feedback inbox so that I can inspect relevant signals before creating an opportunity.

Acceptance criteria:
- Search matches text.
- API supports theme and sentiment filters.
- No-result state is clear.

## Insights

**US-03 — Understand a classification suggestion**  
As a product analyst, I want to see the method and matched terms behind a suggestion so that I can assess its credibility.

Acceptance criteria:
- API returns classification method and matched terms.
- Unmatched feedback is marked Other.
- UI explains that suggestions require human review.

## Opportunities

**US-04 — Create a prioritised opportunity**  
As a product manager, I want to define a customer problem and enter RICE inputs so that prioritisation assumptions are explicit.

Acceptance criteria:
- Reach, impact, confidence, and effort are validated.
- Score is calculated server-side.
- Inputs and score are shown together.

**US-05 — Track an opportunity decision**  
As a product manager, I want to update an opportunity's status so that the team can see whether it is a candidate, planned, in progress, shipped, or dropped.

Acceptance criteria:
- Only supported statuses are accepted.
- Change persists after refresh.

## Experiments

**US-06 — Record a hypothesis**  
As a product manager, I want to capture an if/then/because hypothesis and success metric so that a product bet is testable.

Acceptance criteria:
- Hypothesis and metric are required.
- Baseline, target, and owner can be recorded.
- Status is visible.

**US-07 — Track learning workflow status**  
As a product manager, I want to mark an experiment planned, running, completed, or paused so that the learning queue stays current.

Acceptance criteria:
- Only supported statuses are accepted.
- Change persists after refresh.

## Not in the MVP

- Authentication and role-based permissions.
- Third-party source integrations.
- Evidence-to-opportunity relationships.
- Randomised experiment assignment or statistical inference.
- Model training and production model monitoring.
