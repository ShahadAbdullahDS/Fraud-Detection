import pandas as pd
from src.config import RISK_THRESHOLDS, t


def format_amount(value, lang: str = "ar") -> str:
    if pd.isna(value):
        return t("not_available", lang)
    return f"${value:,.2f}"


def format_hour(value, lang: str = "ar") -> str:
    if pd.isna(value):
        return t("not_available", lang)
    hour = int(value)
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"


def format_number(value, lang: str = "ar") -> str:
    if pd.isna(value):
        return t("not_available", lang)
    if isinstance(value, float):
        if value == int(value):
            return f"{int(value):,}"
        return f"{value:,.2f}"
    return f"{int(value):,}"


def format_percentage(value, lang: str = "ar") -> str:
    if pd.isna(value):
        return t("not_available", lang)
    return f"{value:.2f}%"


def format_cell_value(value, lang: str = "ar") -> str:
    if pd.isna(value) or value == "" or str(value).lower() == "nan":
        return t("not_available", lang)
    return str(value)


def classify_risk(probability: float, lang: str = "ar", low_max: float = None, medium_max: float = None) -> dict:
    if probability < 0:
        return {"level": "unknown", "label": "—", "css_class": ""}

    low_max = RISK_THRESHOLDS["low_max"] if low_max is None else low_max
    medium_max = RISK_THRESHOLDS["medium_max"] if medium_max is None else max(medium_max, low_max)

    if probability <= low_max:
        return {
            "level": "low",
            "label": t("risk_low", lang),
            "css_class": "risk-low",
            "color": "#15803D",
        }
    elif probability <= medium_max:
        return {
            "level": "medium",
            "label": t("risk_medium", lang),
            "css_class": "risk-medium",
            "color": "#B45309",
        }
    else:
        return {
            "level": "high",
            "label": t("risk_high", lang),
            "css_class": "risk-high",
            "color": "#DC2626",
        }


def classify_factor_status(feature_name: str, value, lang: str = "ar") -> dict:
    if pd.isna(value):
        return {"label": t("not_available", lang), "css": "status-normal"}

    if feature_name == "TransactionAmt":
        amt = float(value)
        if amt > 500:
            return {"label": t("high_risk", lang), "css": "status-high"}
        elif amt > 200:
            return {"label": t("needs_review", lang), "css": "status-review"}
        return {"label": t("normal", lang), "css": "status-normal"}

    if feature_name == "hour":
        h = int(value)
        if 1 <= h <= 6:
            return {"label": t("needs_review", lang), "css": "status-review"}
        return {"label": t("normal", lang), "css": "status-normal"}

    return {"label": t("normal", lang), "css": "status-normal"}
