import pytest
import pandas as pd
from src.config import t, TRANSLATIONS


def test_evidence_rail_requires_five_insights():
    from views.overview import build_overview_insights
    eda_two = {
        "findings": [
            {"title": "A", "value": "1", "interpretation": "x"},
            {"title": "B", "value": "2", "interpretation": "y"},
        ]
    }
    insights = build_overview_insights(eda_two, "en")
    assert len(insights) < 5


def test_evidence_rail_builds_five_from_full_eda():
    from views.overview import build_overview_insights
    eda_five = {
        "findings": [
            {"title": f"L{i}", "value": f"V{i}", "interpretation": f"I{i}"}
            for i in range(5)
        ]
    }
    insights = build_overview_insights(eda_five, "en")
    assert len(insights) == 5


def test_no_fabricated_insight_when_missing_fields():
    from views.overview import build_overview_insights
    eda_incomplete = {
        "findings": [
            {"title": "A"},
            {"value": "2"},
            {"title": "C", "value": "3", "interpretation": "z"},
        ]
    }
    insights = build_overview_insights(eda_incomplete, "en")
    assert len(insights) == 1


def test_risk_thresholds_map_correctly():
    from src.formatters import classify_risk
    low = classify_risk(0.10, "en")
    medium = classify_risk(0.45, "en")
    high = classify_risk(0.85, "en")
    assert low["level"] == "low"
    assert medium["level"] == "medium"
    assert high["level"] == "high"


def test_prediction_validation_correct_fraud():
    actual = 1
    predicted = 1
    is_correct = int(actual) == int(predicted)
    assert is_correct is True


def test_prediction_validation_false_negative():
    actual = 1
    predicted = 0
    is_correct = int(actual) == int(predicted)
    assert is_correct is False


def test_prediction_validation_false_positive():
    actual = 0
    predicted = 1
    is_correct = int(actual) == int(predicted)
    assert is_correct is False


def test_all_v3_translations_have_both_languages():
    critical_keys = [
        "correct_classification", "misclassified_case",
        "raises_risk", "reduces_risk", "neutral_context",
        "observed_cues_title", "observed_cues_help",
        "hourly_story_title", "hourly_help",
        "risk_help", "validation_help", "cm_help",
        "f1_help", "auc_help", "recall_help",
        "previous_page", "next_page",
        "false_negative_note", "false_positive_note",
    ]
    for key in critical_keys:
        ar_val = t(key, "ar")
        en_val = t(key, "en")
        assert ar_val and ar_val != key, f"Arabic missing for {key}"
        assert en_val and en_val != key, f"English missing for {key}"


def test_pagination_covers_all_samples():
    total_samples = 20
    cards_per_page = 5
    import math
    total_pages = math.ceil(total_samples / cards_per_page)
    assert total_pages == 4

    seen = set()
    for page in range(total_pages):
        start = page * cards_per_page
        end = min(start + cards_per_page, total_samples)
        for sid in range(start + 1, end + 1):
            seen.add(sid)
    assert len(seen) == total_samples


def test_sample_data_is_balanced():
    from src.data_loader import load_sample_transactions
    samples = load_sample_transactions()
    assert not samples.empty
    fraud_count = (samples["true_label"] == 1).sum()
    legit_count = (samples["true_label"] == 0).sum()
    assert fraud_count == 10
    assert legit_count == 10

    tp = len(samples[(samples["true_label"] == 1) & (samples["model_prediction"] == 1)])
    fn = len(samples[(samples["true_label"] == 1) & (samples["model_prediction"] == 0)])
    tn = len(samples[(samples["true_label"] == 0) & (samples["model_prediction"] == 0)])
    fp = len(samples[(samples["true_label"] == 0) & (samples["model_prediction"] == 1)])
    assert tp == 5
    assert fn == 5
    assert tn == 10
    assert fp == 0
