import pytest
import math
from src.formatters import (
    format_amount, format_hour, format_number,
    format_percentage, format_cell_value, classify_risk,
)


def test_format_amount():
    assert format_amount(1234.56) == "$1,234.56"
    assert format_amount(0) == "$0.00"


def test_format_amount_nan():
    result = format_amount(float("nan"))
    assert result != ""


def test_format_hour_am():
    assert format_hour(3) == "3:00 AM"
    assert format_hour(0) == "12:00 AM"


def test_format_hour_pm():
    assert format_hour(12) == "12:00 PM"
    assert format_hour(15) == "3:00 PM"


def test_format_hour_nan():
    result = format_hour(float("nan"))
    assert result != ""


def test_format_number_int():
    assert format_number(590540) == "590,540"


def test_format_percentage():
    assert format_percentage(3.5) == "3.50%"


def test_format_cell_value_nan():
    result = format_cell_value(float("nan"), "en")
    assert result == "Not available"


def test_format_cell_value_normal():
    assert format_cell_value("visa") == "visa"


def test_classify_risk_low():
    result = classify_risk(0.1, "en")
    assert result["level"] == "low"
    assert "Low" in result["label"]


def test_classify_risk_medium():
    result = classify_risk(0.45, "en")
    assert result["level"] == "medium"


def test_classify_risk_high():
    result = classify_risk(0.85, "en")
    assert result["level"] == "high"
    assert "Suspicious" in result["label"]


def test_classify_risk_boundary_low():
    result = classify_risk(0.30, "en")
    assert result["level"] == "low"


def test_classify_risk_boundary_medium():
    result = classify_risk(0.60, "en")
    assert result["level"] == "medium"


def test_classify_risk_just_above_medium():
    result = classify_risk(0.61, "en")
    assert result["level"] == "high"
