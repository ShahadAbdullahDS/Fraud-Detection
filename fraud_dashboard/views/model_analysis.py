import math
from html import escape

import pandas as pd
import streamlit as st

from src.config import t, RISK_THRESHOLDS
from src.data_loader import load_sample_transactions, load_model_inputs, get_model_input_for_sample, load_metrics
from src.model_service import get_precomputed_probability, predict_fraud_probability
from src.charts import make_gauge, PLOTLY_CONFIG
from src.formatters import classify_risk
from src.case_signals import build_case_signals
from ui.components import (
    ICONS, page_heading, section_header, section_header_html, badge, info_dot,
    info_note, empty_state, step_header,
)
from ui.styles import inject_rules


CARDS_PER_PAGE = 5


def _txt(value):
    if value is None or pd.isna(value) or str(value) == "nan" or str(value) == "":
        return "—"
    return str(value)


def _amount(value):
    return f"${float(value):,.2f}" if pd.notna(value) else "—"


def _hour(value):
    return f"{int(value):02d}:00" if pd.notna(value) else "—"


def _txn_id(value):
    if value is None or pd.isna(value):
        return None
    return str(int(value))


def _risk_bands():
    threshold = (load_metrics() or {}).get("threshold")
    low_max = float(threshold) if threshold is not None else RISK_THRESHOLDS["low_max"]
    medium_max = max(RISK_THRESHOLDS["medium_max"], low_max)
    return low_max, medium_max


def _card_rows(row, lang):
    txn = _txn_id(row.get("TransactionID"))
    return ([(t("card_txn_id", lang), txn)] if txn else []) + [
        (t("card_time", lang), _hour(row.get("hour"))),
        (t("card_product", lang), _txt(row.get("ProductCD"))),
        (t("card_device", lang), _txt(row.get("DeviceType"))),
        (t("card_card", lang), _txt(row.get("card4"))),
        (t("card_email", lang), _txt(row.get("P_emaildomain"))),
    ]


def _init_state():
    for key, default in (("selected_id", None), ("analyzed_id", None), ("card_page", 0)):
        if key not in st.session_state:
            st.session_state[key] = default


def _select(sid):
    st.session_state["selected_id"] = sid


def _page(delta, total_pages):
    st.session_state["card_page"] = min(max(st.session_state["card_page"] + delta, 0), total_pages - 1)


def _analyze():
    st.session_state["analyzed_id"] = st.session_state["selected_id"]
    st.session_state["fresh_analysis"] = True


def _sample_card(row, sid, lang):
    is_selected = st.session_state["selected_id"] == sid
    with st.container(key=f"card_{sid}"):
        chk = f'<span class="chk">{ICONS["check"]}</span>' if is_selected else ""
        rows_html = "".join(
            f'<div class="row"><span>{escape(lbl)}</span><b title="{escape(val)}">{escape(val)}</b></div>'
            for lbl, val in _card_rows(row, lang)
        )
        st.markdown(
            f'<div class="sample"><div class="top"><span>{escape(t("sample_label", lang).format(id=f"{sid:02d}"))}</span>{chk}</div>'
            f'<div class="amt">{_amount(row.get("TransactionAmt"))}</div>'
            f'<div class="rows">{rows_html}</div></div>',
            unsafe_allow_html=True,
        )
        st.button(
            t("selected_btn", lang) if is_selected else t("select_btn", lang),
            key=f"btn_card_{sid}",
            width="stretch",
            type="primary" if is_selected else "secondary",
            on_click=_select,
            args=(sid,),
        )


def render_model_analysis(lang="ar"):
    page_heading(t("review_title", lang), subtitle=t("review_instruction", lang))

    samples = load_sample_transactions()
    model_inputs = load_model_inputs()
    if samples.empty:
        empty_state(t("samples_unavailable", lang))
        return

    _init_state()
    sample_ids = sorted(int(s) for s in samples["sample_id"].tolist())
    total = len(sample_ids)
    total_pages = max(1, math.ceil(total / CARDS_PER_PAGE))
    page = min(st.session_state["card_page"], total_pages - 1)
    st.session_state["card_page"] = page
    start = page * CARDS_PER_PAGE
    end = min(start + CARDS_PER_PAGE, total)
    page_ids = sample_ids[start:end]

    selected = st.session_state["selected_id"]
    if selected is not None:
        inject_rules(
            f".st-key-card_{selected}{{border:2px solid var(--primary) !important;"
            f"box-shadow:0 0 0 4px rgba(45,27,78,.10) !important;padding:13px 13px 11px !important}}"
        )

    with st.container(key="sec_samples"):
        step_header(1, t("step1_title", lang), t("step_range", lang).format(a=start + 1, b=end))

        with st.container(key="carousel"):
            row_cols = st.columns([0.6, 10, 0.6], gap="small", vertical_alignment="center")
            with row_cols[0]:
                with st.container(key="arrow_prev"):
                    st.button(
                        "‹", key="btn_prev", help=t("prev_help", lang),
                        disabled=page == 0, on_click=_page, args=(-1, total_pages),
                    )
            with row_cols[1]:
                card_cols = st.columns(CARDS_PER_PAGE, gap="small")
                for idx, sid in enumerate(page_ids):
                    row = samples[samples["sample_id"] == sid].iloc[0]
                    with card_cols[idx]:
                        _sample_card(row, sid, lang)
            with row_cols[2]:
                with st.container(key="arrow_next"):
                    st.button(
                        "›", key="btn_next", help=t("next_help", lang),
                        disabled=page >= total_pages - 1, on_click=_page, args=(1, total_pages),
                    )

        with st.container(key="car_foot"):
            foot_cols = st.columns([0.6, 6, 4, 0.6], vertical_alignment="center")
            with foot_cols[1]:
                dots = "".join(f'<i class="{"on" if i == page else ""}"></i>' for i in range(total_pages))
                st.markdown(
                    f'<div class="dots">{dots}<span>{escape(t("page_of", lang).format(a=page + 1, b=total_pages))}</span></div>',
                    unsafe_allow_html=True,
                )
            with foot_cols[2]:
                with st.container(key="btn_analyze_wrap"):
                    st.button(
                        f"{t('analyze_btn', lang)} →",
                        key="btn_analyze",
                        type="primary",
                        width="stretch",
                        disabled=selected is None,
                        on_click=_analyze,
                    )

    analyzed = st.session_state["analyzed_id"]
    if analyzed is None:
        empty_state(t("empty_results", lang))
        return

    if selected is not None and selected != analyzed:
        info_note(t("stale_results", lang).format(id=f"{analyzed:02d}"))

    _render_analysis_result(analyzed, samples, model_inputs, lang)


def _compute_probability(sample_id, sample_row, model_inputs):
    probability = get_precomputed_probability(sample_row)
    if probability < 0 and not model_inputs.empty:
        features = get_model_input_for_sample(sample_id, model_inputs)
        if not features.empty:
            probability = predict_fraud_probability(features)
    return probability


def _cue_icon(name):
    low = name.lower()
    if "time" in low or "hour" in low or "الوقت" in name or "ساعة" in name:
        return ICONS["clock"]
    if "amount" in low or "المبلغ" in name:
        return ICONS["dollar"]
    if "email" in low or "بريد" in name:
        return ICONS["mail"]
    return ICONS["dot"]


def _render_analysis_result(sample_id, samples, model_inputs, lang):
    sample_row = samples[samples["sample_id"] == sample_id]
    if sample_row.empty:
        return
    sample_row = sample_row.iloc[0]

    if st.session_state.pop("fresh_analysis", False):
        with st.spinner(t("analyzing", lang)):
            probability = _compute_probability(sample_id, sample_row, model_inputs)
    else:
        probability = _compute_probability(sample_id, sample_row, model_inputs)

    if probability < 0:
        empty_state(t("prob_unavailable", lang))
        return

    step_header(2, t("step2_title", lang).format(id=f"{int(sample_id):02d}"))

    with st.container(key="sec_details"):
        section_header(t("details_title", lang))
        cells = [
            ("det_sample_id", f"{int(sample_row['sample_id']):02d}"),
            *([("det_txn_id", _txn_id(sample_row.get("TransactionID")))] if _txn_id(sample_row.get("TransactionID")) else []),
            ("det_amount", _amount(sample_row.get("TransactionAmt"))),
            ("det_time", _hour(sample_row.get("hour"))),
            ("det_product", _txt(sample_row.get("ProductCD"))),
            ("det_device", _txt(sample_row.get("DeviceType"))),
            ("det_card", _txt(sample_row.get("card6"))),
            ("det_network", _txt(sample_row.get("card4"))),
            ("det_email", _txt(sample_row.get("P_emaildomain"))),
        ]
        st.markdown(
            f'<div class="details" style="--n:{len(cells)}">' + "".join(
                f'<div><span>{escape(t(k, lang))}</span><b title="{escape(v)}">{escape(v)}</b></div>' for k, v in cells
            ) + "</div>",
            unsafe_allow_html=True,
        )

    low_max, medium_max = _risk_bands()
    risk = classify_risk(probability, lang, low_max=low_max, medium_max=medium_max)
    risk_help = t("risk_help_dynamic", lang).format(t=f"{low_max * 100:.1f}", h=f"{medium_max * 100:.0f}")
    result_cols = st.columns(2, gap="large")

    with result_cols[0]:
        with st.container(key="sec_gauge"):
            section_header(t("estimated_fraud_risk", lang), info=risk_help)
            st.plotly_chart(
                make_gauge(probability, lang, low_max=low_max, medium_max=medium_max),
                width="stretch", config=PLOTLY_CONFIG, key="chart_gauge",
            )
            icon = {"low": ICONS["ok"], "medium": ICONS["warn"], "high": ICONS["warn"]}.get(risk["level"], "")
            st.markdown(
                f'<div class="verdict-wrap"><span class="verdict {risk["level"]}">{icon}{escape(risk["label"])}</span></div>'
                f'<div class="gauge-caption">{escape(t("model_recommendation_note", lang))}</div>',
                unsafe_allow_html=True,
            )

    with result_cols[1]:
        with st.container(key="sec_cues"):
            section_header(t("observed_cues_title", lang), subtitle=t("cues_note", lang))
            cues = build_case_signals(sample_row, probability, lang)
            if not cues:
                empty_state(t("no_cues", lang))
            else:
                html = '<div class="cues">'
                for cue in cues:
                    direction = cue.get("direction", "neutral")
                    if direction == "raises":
                        b = badge(f"↑ {t('raises_risk', lang)}", "fraud")
                    elif direction == "reduces":
                        b = badge(f"↓ {t('reduces_risk', lang)}", "legit")
                    else:
                        b = badge(f"— {t('neutral_context', lang)}", "neutral")
                    name = cue.get("name", "")
                    html += (
                        f'<div class="cue"><span class="ic">{_cue_icon(name)}</span>'
                        f'<div><div class="k">{escape(name)}</div>'
                        f'<div class="v">{escape(str(cue.get("value", "")))}</div>'
                        f'<div class="ex">{escape(cue.get("interpretation", ""))}</div></div>{b}</div>'
                    )
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

    true_label = sample_row.get("true_label", sample_row.get("isFraud"))
    pred_label = sample_row.get("model_prediction")
    if pd.notna(true_label) and pd.notna(pred_label):
        _render_validation(true_label, pred_label, lang)


def _render_validation(actual, predicted, lang):
    is_fraud_actual = int(actual) == 1
    is_fraud_pred = int(predicted) == 1
    is_correct = is_fraud_actual == is_fraud_pred

    actual_badge = badge(t("is_fraud", lang) if is_fraud_actual else t("is_legit", lang), "fraud" if is_fraud_actual else "legit")
    pred_badge = badge(t("is_fraud", lang) if is_fraud_pred else t("is_legit", lang), "fraud" if is_fraud_pred else "legit")

    if is_correct:
        cls, icon, title, title_badge = "correct", ICONS["alert_ok"], t("correct_classification", lang), ""
        foot = t("correct_match_note", lang)
    else:
        cls, icon, title = "wrong", ICONS["alert_wrong"], t("misclassified_case", lang)
        if is_fraud_actual and not is_fraud_pred:
            title_badge = badge(t("false_negative", lang), "amber")
            foot = t("false_negative_note", lang)
        else:
            title_badge = badge(t("false_positive", lang), "amber")
            foot = t("false_positive_note", lang)

    st.markdown(
        f'<div class="alert {cls}"><span class="ai">{icon}</span>'
        f'<div class="body"><div class="h3">{escape(title)}{title_badge}</div>'
        f'<div class="cmp"><span>{escape(t("actual_outcome_lbl", lang))}</span><b>{actual_badge}</b>'
        f'<span>{escape(t("model_prediction_lbl", lang))}</span><b>{pred_badge}</b></div>'
        f'<p class="foot">{escape(foot)}</p></div>'
        f'{info_dot(t("validation_help", lang), title)}</div>',
        unsafe_allow_html=True,
    )
