import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.analysis import analyze_feedback


def test_reliability_feedback_is_classified():
    result = analyze_feedback("The dashboard crashes and loading is slow.")
    assert result["theme"] == "Reliability"
    assert result["sentiment"] == "negative"
    assert result["method"] == "keyword baseline v1"


def test_positive_feedback_is_positive():
    result = analyze_feedback("The setup was easy and the tutorial was helpful.")
    assert result["theme"] == "Onboarding"
    assert result["sentiment"] == "positive"


def test_unmatched_feedback_is_kept_for_review():
    result = analyze_feedback("Could you add support for my unusual use case?")
    assert result["theme"] == "Other"
    assert result["confidence"] == 0.35


def test_sentiment_tokenisation_handles_punctuation_and_word_forms():
    result = analyze_feedback("The dashboard crashes, and loading is slow.")
    assert result["sentiment"] == "negative"
