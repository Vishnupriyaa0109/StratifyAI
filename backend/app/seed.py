from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Feedback, Opportunity, Experiment
from .analysis import analyze_feedback

DEMO_FEEDBACK = [
    ("In-app", "SMB", "I got stuck during onboarding because I could not understand which data source to connect first."),
    ("Support", "Mid-market", "The dashboard takes too long to load when I filter a large date range."),
    ("Review", "Enterprise", "The weekly report is useful, but exporting a filtered view is difficult."),
    ("Survey", "SMB", "The setup checklist made our first week much easier."),
    ("Support", "Mid-market", "Our CRM integration breaks and we have to reconnect it every few days."),
    ("In-app", "Enterprise", "I love the new report layout; it is clear and easy to share."),
    ("Review", "SMB", "The pricing is expensive for a small team that only needs two reports."),
    ("Survey", "Mid-market", "I cannot tell whether the numbers in the dashboard are updated today or yesterday."),
    ("Support", "Enterprise", "We manually combine exports from three tools. This workflow is frustrating."),
    ("In-app", "SMB", "The first-time setup was simple and the tutorial was helpful."),
    ("Review", "Mid-market", "The application crashed while saving a report and I lost my filters."),
    ("Survey", "Enterprise", "We need better filters to understand adoption by customer segment."),
    ("Support", "SMB", "The invoice is confusing and I do not understand the plan limits."),
    ("In-app", "Mid-market", "I want an easier way to automate recurring reports."),
    ("Review", "Enterprise", "The platform is reliable this month and our team saved time."),
    ("Survey", "SMB", "I cannot find the onboarding guide after creating my account."),
    ("Support", "Mid-market", "The integration is useful, but the initial configuration is difficult."),
    ("In-app", "Enterprise", "The dashboard charts are clear, but I need to export the underlying data."),
    ("Review", "SMB", "The subscription cost feels high compared with the features we use."),
    ("Survey", "Mid-market", "The report loads fast now and the filters are intuitive."),
]

DEMO_OPPORTUNITIES = [
    ("Reduce onboarding drop-off", "New teams struggle to choose and connect their first data source, delaying first value.", "Onboarding", 80, 2.5, 0.8, 3, "Candidate"),
    ("Improve dashboard load time", "Users wait too long when exploring large date ranges, reducing trust and repeat usage.", "Reliability", 65, 3, 0.9, 5, "Candidate"),
    ("Make report exports flexible", "Teams cannot reliably export filtered views and resort to manual work.", "Reporting", 55, 2, 0.7, 2, "Planned"),
    ("Clarify plan limits and pricing", "Small teams cannot predict which plan supports their reporting needs.", "Pricing", 35, 1.5, 0.6, 2, "Candidate"),
]

DEMO_EXPERIMENTS = [
    ("Guided first data-source setup", "If we show a recommended first data source and a three-step checklist, more new workspaces will complete setup.", "Workspace setup completion", 42, 55, "Running", "Growth"),
    ("Filtered export preview", "If users can preview selected columns and filters before export, successful report exports will increase.", "Successful export rate", 68, 78, "Planned", "Product"),
    ("Dashboard freshness label", "If each dashboard shows a clear last-refreshed timestamp, data freshness support contacts will decrease.", "Freshness-related tickets / week", 24, 16, "Planned", "Analytics"),
]


def seed_demo_data(db: Session):
    if db.scalar(select(Feedback.id).limit(1)) is not None:
        return
    for source, segment, text in DEMO_FEEDBACK:
        result = analyze_feedback(text)
        db.add(Feedback(source=source, segment=segment, text=text, theme=result["theme"], sentiment=result["sentiment"]))
    for title, problem, theme, reach, impact, confidence, effort, status in DEMO_OPPORTUNITIES:
        db.add(Opportunity(title=title, problem_statement=problem, theme=theme, reach=reach, impact=impact, confidence=confidence, effort=effort, status=status))
    for title, hypothesis, metric, baseline, target, status, owner in DEMO_EXPERIMENTS:
        db.add(Experiment(title=title, hypothesis=hypothesis, success_metric=metric, baseline_value=baseline, target_value=target, status=status, owner=owner))
    db.commit()
