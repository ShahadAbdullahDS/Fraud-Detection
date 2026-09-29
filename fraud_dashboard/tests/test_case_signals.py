import pytest
import pandas as pd
import src.case_signals as case_signals
from src.case_signals import (
    build_case_signals, has_local_explanation, load_context_profiles,
)


FIXED_PROFILE = {
    "thresholds": {
        "baseline_fraud_rate": 3.5,
        "high_risk_hours": {"start": 5, "end": 9, "peak": 7, "peak_rate": 10.6},
        "hourly_rates": {"14": 2.4, "7": 10.6},
        "amount_bands": {
            "low": {"max": 100, "fraud_rate": 1.5},
            "medium": {"min": 100, "max": 500, "fraud_rate": 3.8},
            "high": {"min": 500, "max": 2000, "fraud_rate": 7.2},
            "very_high": {"min": 2000, "fraud_rate": 9.8},
        },
        "high_risk_email_domains": ["protonmail.com"],
        "common_safe_domains": ["gmail.com"],
    }
}


@pytest.fixture
def fixed_profile(monkeypatch):
    monkeypatch.setattr(case_signals, "load_context_profiles", lambda: FIXED_PROFILE)


def test_context_profiles_load():
    profiles = load_context_profiles()
    assert profiles
    assert "thresholds" in profiles
    thresholds = profiles["thresholds"]
    assert "high_risk_hours" in thresholds
    assert "amount_bands" in thresholds


def test_signal_source_is_data_context_not_local():
    assert has_local_explanation() is False


def test_high_risk_hour_raises_risk(fixed_profile):
    row = pd.Series({"hour": 7, "TransactionAmt": 45.0, "P_emaildomain": "gmail.com"})
    signals = build_case_signals(row, 0.75, "en")
    assert len(signals) > 0
    hour_signal = next((s for s in signals if "Time" in s["name"] or "hour" in s["name"].lower()), None)
    assert hour_signal is not None
    assert hour_signal["direction"] == "raises"


def test_low_amount_reduces_risk(fixed_profile):
    row = pd.Series({"hour": 14, "TransactionAmt": 45.0, "P_emaildomain": "gmail.com"})
    signals = build_case_signals(row, 0.15, "en")
    amt_signal = next((s for s in signals if "Amount" in s["name"]), None)
    assert amt_signal is not None
    assert amt_signal["direction"] == "reduces"


def test_high_amount_raises_risk(fixed_profile):
    row = pd.Series({"hour": 14, "TransactionAmt": 3500.0, "P_emaildomain": "gmail.com"})
    signals = build_case_signals(row, 0.75, "en")
    amt_signal = next((s for s in signals if "Amount" in s["name"]), None)
    assert amt_signal is not None
    assert amt_signal["direction"] == "raises"


def test_max_three_signals():
    row = pd.Series({"hour": 7, "TransactionAmt": 3500.0, "P_emaildomain": "protonmail.com"})
    signals = build_case_signals(row, 0.75, "en")
    assert len(signals) <= 3


def test_no_v_features_in_signals():
    row = pd.Series({"hour": 7, "TransactionAmt": 45.0, "V258": 1.5, "V317": 0.3})
    signals = build_case_signals(row, 0.75, "en")
    for signal in signals:
        name = signal.get("name", "")
        assert not name.startswith("V")


def test_arabic_signals_non_empty():
    row = pd.Series({"hour": 7, "TransactionAmt": 3500.0, "P_emaildomain": "protonmail.com"})
    signals = build_case_signals(row, 0.75, "ar")
    assert len(signals) > 0
    for signal in signals:
        assert signal.get("interpretation")


def test_amount_direction_follows_band_rate(fixed_profile):
    row = pd.Series({"hour": 14, "TransactionAmt": 250.0})
    signals = build_case_signals(row, 0.2, "en")
    amt_signal = next(s for s in signals if "Amount" in s["name"])
    assert amt_signal["direction"] == "neutral"
    assert "3.8%" in amt_signal["interpretation"]


def test_classify_risk_uses_model_threshold():
    from src.formatters import classify_risk
    assert classify_risk(0.25, "en", low_max=0.2, medium_max=0.6)["level"] == "medium"
    assert classify_risk(0.15, "en", low_max=0.2, medium_max=0.6)["level"] == "low"
