"""Transparent baseline feedback analysis; deliberately not presented as a trained ML model."""

import re

THEME_KEYWORDS = {
    "Onboarding": ["onboard", "setup", "sign up", "sign-up", "first time", "getting started", "tutorial"],
    "Reliability": ["crash", "broken", "slow", "loading", "bug", "error", "timeout", "unavailable"],
    "Pricing": ["price", "pricing", "expensive", "cost", "bill", "subscription", "plan", "invoice"],
    "Workflow": ["workflow", "integration", "integrate", "export", "import", "automation", "manual", "duplicate"],
    "Reporting": ["report", "dashboard", "analytics", "metric", "filter", "chart", "data"],
}
NEGATIVE_TERMS = {
    "confusing", "difficult", "hard", "slow", "broken", "crash", "crashes",
    "crashed", "crashing", "bug", "bugs", "error", "errors", "expensive",
    "missing", "frustrating", "annoying", "cannot", "failed", "fail", "fails",
    "issue", "problem", "unusable", "timeout",
}
POSITIVE_TERMS = {
    "easy", "helpful", "useful", "fast", "love", "great", "excellent",
    "simple", "clear", "intuitive", "reliable", "saved", "amazing", "smooth",
}


def analyze_feedback(text: str) -> dict:
    normalized = text.lower()
    theme_scores = {
        theme: sum(1 for keyword in keywords if keyword in normalized)
        for theme, keywords in THEME_KEYWORDS.items()
    }
    best_theme = max(theme_scores, key=theme_scores.get)
    matched = theme_scores[best_theme]
    theme = best_theme if matched else "Other"

    # Strip punctuation so sentence-final terms are still counted.
    words = set(re.findall(r"[a-z0-9]+", normalized))
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
