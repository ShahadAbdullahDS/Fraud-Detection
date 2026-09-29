import json
import pandas as pd
from pathlib import Path
from src.config import t, DATA_DIR


CONTEXT_PROFILES_PATH = DATA_DIR / "context_profiles.json"


def load_context_profiles():
    if not CONTEXT_PROFILES_PATH.exists():
        return {}
    with open(CONTEXT_PROFILES_PATH, "r") as f:
        return json.load(f)


RAISE_RATIO = 1.3
REDUCE_RATIO = 0.8


def _baseline(profile):
    return float(profile.get("baseline_fraud_rate", 3.5))


def _direction(rate, baseline):
    if rate is None or baseline <= 0:
        return "neutral"
    ratio = rate / baseline
    if ratio >= RAISE_RATIO:
        return "raises"
    if ratio <= REDUCE_RATIO:
        return "reduces"
    return "neutral"


def _iso(text):
    return "\u2066" + str(text) + "\u2069"


def _cue(name, value, direction, text_en, text_ar, lang):
    return {
        "name": name,
        "value": value,
        "direction": direction,
        "css_class": f"cue-{direction}",
        "interpretation": text_ar if lang == "ar" else text_en,
    }


def _amount_band(amt, bands):
    ordered = [
        ("low", None, bands.get("low", {}).get("max", 100)),
        ("medium", bands.get("medium", {}).get("min", 100), bands.get("medium", {}).get("max", 500)),
        ("high", bands.get("high", {}).get("min", 500), bands.get("high", {}).get("max", 2000)),
        ("very_high", bands.get("very_high", {}).get("min", 2000), None),
    ]
    for key, lo, hi in ordered:
        if (lo is None or amt >= lo) and (hi is None or amt < hi):
            return key, lo, hi, bands.get(key, {}).get("fraud_rate")
    return None, None, None, None


def _range_label(lo, hi):
    if lo is None:
        return f"<${hi:,}"
    if hi is None:
        return f"${lo:,}+"
    return f"${lo:,}–${hi:,}"


def _amount_cue(amount, profile, lang):
    if amount is None or pd.isna(amount):
        return None
    amt = float(amount)
    base = _baseline(profile)
    key, lo, hi, rate = _amount_band(amt, profile.get("amount_bands", {}))
    if key is None or rate is None:
        return None
    band = _range_label(lo, hi)
    direction = _direction(rate, base)
    return _cue(
        t("amount", lang), f"${amt:,.2f}", direction,
        f"Transactions in the {band} range have a {rate:.1f}% fraud rate, versus {base:.1f}% overall.",
        f"المعاملات في نطاق {_iso(band)} معدل احتيالها {_iso(f'{rate:.1f}%')} مقابل {_iso(f'{base:.1f}%')} بشكل عام.",
        lang,
    )


def _hour_cue(hour, profile, lang):
    if hour is None or pd.isna(hour):
        return None
    h = int(hour)
    base = _baseline(profile)
    hours = profile.get("high_risk_hours", {})
    start = int(hours.get("start", 5))
    end = int(hours.get("end", 9))
    label = hours.get("label") or f"{start:02d}:00-{(end + 1) % 24:02d}:00"
    rate = profile.get("hourly_rates", {}).get(str(h))
    rate_en = f" ({rate:.1f}% fraud rate at this hour)" if rate is not None else ""
    rate_ar = f" (معدل الاحتيال في هذه الساعة {_iso(f'{rate:.1f}%')})" if rate is not None else ""

    if start <= h <= end:
        return _cue(
            t("hour_label", lang), f"{h:02d}:00", "raises",
            f"This time falls inside the observed high-risk window ({label}){rate_en}.",
            f"هذه الساعة تقع ضمن نافذة الخطورة المرصودة ({_iso(label)}){rate_ar}.",
            lang,
        )
    direction = _direction(rate, base) if rate is not None else "neutral"
    if direction == "raises":
        text_en, text_ar = "Outside the main high-risk window, but still above the overall fraud rate", "خارج نافذة الخطورة الرئيسية لكن أعلى من المعدل العام"
    elif direction == "reduces":
        text_en, text_ar = "This time is outside the observed high-risk window in the data", "ساعة خارج نافذة الخطورة الرئيسية في البيانات"
    else:
        text_en, text_ar = "Outside the main high-risk window, close to the overall fraud rate", "خارج نافذة الخطورة الرئيسية وقريبة من المعدل العام"
    return _cue(t("hour_label", lang), f"{h:02d}:00", direction, f"{text_en}{rate_en}.", f"{text_ar}{rate_ar}.", lang)


def _email_cue(email, profile, lang):
    if email is None or pd.isna(email) or str(email) in ("nan", ""):
        return None
    e = str(email).lower()
    rates = profile.get("email_rates", {})
    rate = rates.get(e)
    rate_en = f" ({rate:.1f}% fraud rate)" if rate is not None else ""
    rate_ar = f" (معدل احتيال {_iso(f'{rate:.1f}%')})" if rate is not None else ""

    if e in profile.get("high_risk_email_domains", []):
        return _cue(
            t("email_domain", lang), e, "raises",
            f"Email domain shows an elevated fraud concentration in the available data{rate_en}.",
            f"نطاق بريد يظهر تركيزاً مرتفعاً للاحتيال في البيانات المتاحة{rate_ar}.",
            lang,
        )
    if e in profile.get("common_safe_domains", []):
        return _cue(
            t("email_domain", lang), e, "reduces",
            f"A common domain in legitimate transactions{rate_en}.",
            f"نطاق بريد شائع في المعاملات الشرعية{rate_ar}.",
            lang,
        )
    return None


def build_case_signals(sample_row, probability, lang="en", max_signals=3):
    profile_data = load_context_profiles()
    if not profile_data:
        return []
    profile = profile_data.get("thresholds", {})

    candidates = []

    hour_signal = _hour_cue(sample_row.get("hour"), profile, lang)
    if hour_signal:
        candidates.append(hour_signal)

    amt_signal = _amount_cue(sample_row.get("TransactionAmt"), profile, lang)
    if amt_signal:
        candidates.append(amt_signal)

    email_signal = _email_cue(sample_row.get("P_emaildomain"), profile, lang)
    if email_signal:
        candidates.append(email_signal)

    priority = {"raises": 0, "reduces": 1, "neutral": 2}
    candidates.sort(key=lambda x: priority.get(x["direction"], 3))

    return candidates[:max_signals]


def has_local_explanation():
    return False


def get_signal_source_label(lang="en"):
    if has_local_explanation():
        return t("why_this_result", lang)
    return t("observed_cues_title", lang)
