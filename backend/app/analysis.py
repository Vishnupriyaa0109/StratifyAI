"""Transparent baseline feedback analysis; deliberately not presented as a trained ML model."""

THEME_KEYWORDS = {
    "Onboarding": ["onboard", "setup", "sign up", "sign-up", "first time", "getting started", "tutorial"],
    "Reliability": ["crash", "bug", "error", "broken", "slow", "loading", "timeout", "unavailable"],
    "Pricing": ["price", "pricing", "expensive", "cost", "bill", "subscription", "plan", "invoice"],
    "Workflow": ["workflow", "integration", "integrate", "export", "import", "automation", "manual", "duplicate"],
    "Reporting": ["report", "dashboard", "analytics", "metric", "filter", "chart", "data"],
}
NEGATIVE_TERMS = {"confusing", "difficult", "hard", "slow", "broken", "crash", "bug", "error", "expensive", "missing", "frustrating", "annoying", "cannot", "can't", "failed", "fail", "issue", "problem", "unusable"}
POSITIVE_TERMS = {"easy", "helpful", "useful", "fast", "love", "great", "excellent", "simple", "clear", "intuitive", "reliable", "saved", "amazing", "smooth"}


def analyze_feedback(text: str) -> dict:
    normalized = text.lower()
    theme_scores = {
        theme: sum(1 for keyword in keywords if keyword in normalized)
        for theme, keywords in THEME_KEYWORDS.items()
    }
    best_theme = max(theme_scores, key=theme_scores.get)
    matched = theme_scores[best_theme]
    theme = best_theme if matched else "Other"

    words = set(normalized.replace("'", "").replace("-", " ").split())
    negative = len(words & NEGATIVE_TERMS)
    positive = len(words & POSITIVE_TERMS)
    sentiment = "negative" if negative > positive else "positive" if positive > negative else "neutral"
    matched_terms = [term for term in THEME_KEYWORDS.get(theme, []) if term in normalized]
    explanation = (
        f"Theme '{theme}' matched: {', '.join(matched_terms[:3])}."
        if matched_terms else "No theme keyword matched; routed to Other for human review."
    )
    return {
        "theme": theme,
        "sentiment": sentiment,
        "confidence": round(min(0.95, 0.55 + 0.1 * max(0, matched - 1)), 2) if matched else 0.35,
        "explanation": explanation,
        "method": "keyword baseline v1",
    }
