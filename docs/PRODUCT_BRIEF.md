# Product brief — StratifyAI

## Product vision
Help product teams make fewer opinion-led decisions and more evidence-linked decisions by connecting the voice of the customer to the product backlog and learning loop.

**Tagline:** From Customer Voices to Confident Product Decisions.

## Problem statement
Customer feedback is distributed across support tickets, surveys, reviews, and in-product channels. Product managers can struggle to detect repeated pain points, understand who is affected, explain prioritisation, and connect shipped work to measurable learning.

## Initial target users (hypotheses to validate)
These are working personas for discovery, not research findings.

### 1. Product manager at a growing SaaS company
- **Job to be done:** Understand which customer problems deserve attention this cycle.
- **Current workaround:** Spreadsheets, Slack threads, ticket tags, and anecdotal requests.
- **Pain hypothesis:** It takes too long to consolidate evidence and explain prioritisation.
- **Desired outcome:** A traceable shortlist of problems with evidence, assumptions, and next steps.

### 2. Customer success / support lead
- **Job to be done:** Make recurring customer friction visible to product and engineering.
- **Current workaround:** Escalating individual tickets and preparing periodic summaries.
- **Pain hypothesis:** Repeated issues lose context as they move between teams.
- **Desired outcome:** Feedback grouped by theme and customer segment, while preserving source text.

### 3. Product / business founder at an early-stage company
- **Job to be done:** Focus limited engineering time on high-value customer problems.
- **Current workaround:** Direct conversations, founder intuition, and a small issue tracker.
- **Pain hypothesis:** Prioritisation criteria are inconsistent and difficult to revisit.
- **Desired outcome:** A lightweight, repeatable decision process without enterprise tooling overhead.

## Value proposition
A focused workflow that makes feedback easier to review, opportunities easier to compare, and experiments easier to track — while keeping source evidence and assumptions visible.

## MVP scope
**In scope:** manual feedback capture, source/segment labels, heuristic theme/sentiment suggestions, dashboard aggregates, RICE backlog, experiment hypothesis and metric tracking.

**Out of scope (initial release):** external platform connectors, predictive recommendations, autonomous roadmap decisions, production ML, authentication and team permissions, experiment randomisation/analysis, billing.

## Product principles
1. **Evidence before scores:** a high prioritisation score is not proof of customer value.
2. **Explain suggestions:** users should know why a label was suggested.
3. **Human review stays in control:** automation assists, product teams decide.
4. **Keep the workflow lightweight:** make one useful next action obvious.
5. **Be honest about uncertainty:** distinguish sample data, assumptions, hypotheses, and measured outcomes.

## Primary risks and assumptions
| Assumption / risk | Why it matters | How to validate |
|---|---|---|
| Feedback consolidation is a frequent PM pain | Determines problem intensity | Discovery interviews and workflow observation |
| Teams want one workflow from evidence to experiments | Determines product scope | Test a clickable prototype and task completion |
| Simple theme suggestions are trusted when explainable | Determines automation approach | Compare suggestions with human labels |
| RICE is used consistently enough to help | Determines prioritisation UX | Observe scoring sessions and calibration |
| Manual import is sufficient for first value | Determines MVP activation | Concierge pilot with sample CSVs |

## Positioning
StratifyAI is a product decision workspace, not just a sentiment dashboard. Its differentiator is the intended traceability from original feedback to reviewed insight, prioritised problem, experiment, and decision.
