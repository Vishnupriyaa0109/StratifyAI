# Product metrics and experimentation

This document proposes a measurement model for future validation. The demo's sample counts, experiment baselines, and targets are synthetic illustrations, not observed product results.

## Product outcome
**North-star metric hypothesis:** Reviewed customer problems that lead to a documented product decision per active workspace per month.

This metric is a hypothesis. It rewards evidence-to-decision flow, not raw feedback volume.

## Metric tree

| Layer | Metric | Definition to validate |
|---|---|---|
| Acquisition / entry | Connected or created workspaces | Workspaces that begin setup |
| Activation | First reviewed insight | Workspace has feedback and a human-reviewed theme |
| Core value | Evidence-linked opportunities | Prioritised opportunities linked to supporting feedback |
| Decision quality proxy | Review / override rate | Suggested labels accepted or edited after human review |
| Learning | Experiments with documented decisions | Experiment completion with result and next action |
| Retention | Weekly active product workspaces | Workspaces returning to review or update decisions |

## Guardrail metrics
- Feedback records with missing source/segment context.
- Percentage of suggested labels overridden by a reviewer.
- Time spent correcting classifications.
- Duplicate feedback rate.
- Data deletion and access-control incidents.
- User-reported trust or usability issues.

## Experiment template
**Problem:** Describe the observed user pain.  
**Target segment:** Specify eligible users/workspaces.  
**Hypothesis:** If we [change], then [measurable outcome] will [direction], because [reason].  
**Primary metric:** One metric directly tied to the intended outcome.  
**Guardrails:** Quality, reliability, privacy, or workload measures that must not deteriorate.  
**Baseline:** Measured before the change, with period and cohort.  
**Target / decision threshold:** Set before observing results.  
**Method:** A/B test, staged rollout, usability test, or qualitative pilot.  
**Sample / duration:** Based on expected effect, variance, traffic, and decision risk.  
**Readout:** Results, uncertainty, segments, limitations, decision, and follow-up.

## Illustrative experiment ideas (not executed)
1. **Guided first data-source setup** — test whether a recommended first connection and checklist improve setup completion.
2. **Filtered export preview** — test whether a preview reduces failed or repeated exports.
3. **Dashboard freshness label** — test whether visible data freshness reduces freshness-related support contacts.

## Experiment decision rules
- Define eligibility and exclusions before launch.
- Select one primary metric; avoid choosing a metric after seeing results.
- Include guardrails and monitor unintended consequences.
- Do not call a result statistically significant unless the design and analysis support that claim.
- Record null and negative results.
- State whether evidence supports ship, iterate, rollback, or further investigation.
