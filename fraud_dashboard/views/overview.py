from html import escape

import streamlit as st

from src.config import t
from src.data_loader import (
    load_eda_summary, load_hourly_fraud, load_metrics, load_feature_importance, load_fraud_stats,
)
from src.charts import (
    make_hourly_story, make_confusion_matrix, make_feature_importance,
    PLOTLY_CONFIG,
)
from ui.components import (
    page_heading, section_header, metric_row, kpi_grid, info_note, empty_state,
)


KPI_ORDER = [
    ("Dataset coverage", False),
    ("Baseline fraud rate", False),
    ("Average fraud amount", False),
    ("Highest-risk hour", True),
    ("Peak fraud rate", True),
    ("High-risk window", True),
]


def build_overview_insights(eda, lang):
    findings = eda.get("findings", []) if eda else []
    insights = []
    for finding in findings:
        label = finding.get("title_ar" if lang == "ar" else "title", "")
        value = finding.get("value", "")
        interp = finding.get("interpretation_ar" if lang == "ar" else "interpretation", "")
        if label and value and interp:
            insights.append({
                "label": label,
                "value": value,
                "interpretation": interp,
                "key": finding.get("title", label),
                "tooltip": finding.get("body_ar" if lang == "ar" else "body", ""),
            })
    return insights


def _ordered_kpis(insights):
    by_key = {i["key"]: i for i in insights}
    ordered = []
    for key, hl in KPI_ORDER:
        if key in by_key:
            ordered.append((by_key.pop(key), hl))
    for rest in by_key.values():
        ordered.append((rest, False))
    return ordered


def _hourly_context(eda):
    stats = load_fraud_stats() or {}
    eda = eda or {}
    baseline = eda.get("baseline_rate", stats.get("fraud_rate_pct"))
    win = eda.get("high_risk_window") or {}
    window = (int(win["start"]), int(win["end"])) if "start" in win and "end" in win else None
    level = eda.get("high_risk_level")
    return {
        "baseline": float(baseline) if baseline is not None else None,
        "window": window,
        "level": float(level) if level is not None else None,
    }


def _plot(fig, key):
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG, key=key)


def render_overview(lang="ar"):
    page_heading(t("overview_title", lang), subtitle=t("overview_subtitle", lang))

    metrics = load_metrics()
    if metrics:
        f1 = metrics.get("f1", 0)
        auc = metrics.get("auc", 0)
        recall = metrics.get("recall", 0)
        with st.container(key="sec_quality"):
            section_header(t("model_quality_title", lang), info=t("model_quality_help", lang))
            metric_row([
                ("F1-Score", f"{f1:.2f}", t("f1_tt", lang).format(v=f"{f1:.2f}")),
                ("ROC-AUC", f"{auc:.2f}", t("auc_tt", lang).format(v=f"{auc:.2f}")),
                ("Recall", f"{recall:.2f}", t("recall_tt", lang).format(v=f"{recall:.2f}", p=f"{recall * 100:.0f}")),
            ])

    eda = load_eda_summary()
    insights = build_overview_insights(eda, lang)
    if len(insights) >= 6:
        kpi_grid([
            dict(
                label=ins["label"],
                value=ins["value"],
                description=ins["interpretation"],
                highlight=hl,
                tooltip=ins.get("tooltip") or None,
            )
            for ins, hl in _ordered_kpis(insights)[:6]
        ])

    hourly_df = load_hourly_fraud()
    if not hourly_df.empty:
        peak_row = hourly_df.loc[hourly_df["fraud_rate"].idxmax()]
        peak_rate = float(peak_row["fraud_rate"])
        peak_hour = f"{int(peak_row['hour']):02d}:00"
        with st.container(key="sec_hourly"):
            section_header(
                t("hourly_story_title", lang),
                subtitle=t("hourly_key_note", lang),
                info=t("hourly_help", lang),
            )
            st.markdown(
                f'<div class="fsd-headline"><span class="n">{peak_rate:.1f}%</span>'
                f'<span class="t">{escape(t("hourly_headline", lang).format(hour=peak_hour))}</span></div>',
                unsafe_allow_html=True,
            )
            _plot(make_hourly_story(hourly_df, lang, **_hourly_context(eda)), "chart_hourly")

    if metrics:
        with st.container(key="sec_cm"):
            section_header(
                t("confusion_matrix", lang),
                subtitle=t("cm_subtitle", lang),
                info=t("cm_help", lang),
            )
            cm_cols = st.columns([2, 3], gap="large", vertical_alignment="center")
            with cm_cols[0]:
                _plot(make_confusion_matrix(metrics, lang), "chart_cm")
            with cm_cols[1]:
                cards = [
                    ("True Neg", "cm_tn_q", "cm_tn_res", "ok", "var(--primary)", ""),
                    ("True Pos", "cm_tp_q", "cm_tp_res", "ok", "var(--primary)", ""),
                    ("False Pos", "cm_fp_q", "cm_fp_res", "bad", "var(--red-soft)", ""),
                    ("False Neg", "cm_fn_q", "cm_fn_res", "bad", "var(--red-soft)", "color:var(--red);"),
                ]
                html = '<div class="cm-grid">'
                for name, q_key, res_key, cls, sw, name_style in cards:
                    sw_border = "border:1px solid #f0b8b3;" if cls == "bad" else ""
                    html += (
                        f'<div class="cm-item"><i class="sw" style="background:{sw};{sw_border}"></i>'
                        f'<div><b style="{name_style}">{name}</b>'
                        f'<span class="q">{t(q_key, lang)}</span>'
                        f'<span class="res {cls}">{escape(t(res_key, lang))}</span></div></div>'
                    )
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

    with st.container(key="adv_exp"):
        with st.expander(t("advanced_evidence", lang)):
            st.markdown(f'<div class="fsd-cap">{escape(t("adv_caption", lang))}</div>', unsafe_allow_html=True)
            fi_df = load_feature_importance()
            if not fi_df.empty:
                info_note(t("fi_limitation", lang))
                _plot(make_feature_importance(fi_df, lang), "chart_fi")
            else:
                empty_state(t("fi_unavailable", lang))
