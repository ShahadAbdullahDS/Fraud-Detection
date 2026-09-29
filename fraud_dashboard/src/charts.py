import re

import plotly.graph_objects as go

from src.config import t


PLOTLY_CONFIG = {"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showTips": False}
FONT_FAMILY = "Saira, Tajawal, system-ui, sans-serif"
INK = "#1b1530"
INK_2 = "#4b5064"
INK_3 = "#6b7084"
GRID = "#eceef3"
RED = "#c8281e"
PRIMARY = "#2d1b4e"


_NUM_RUN = re.compile(r"[$\d][\d:.,%–\-$]*[\d%]|\(%\)|\d")


def _bidi(text, lang):
    if lang != "ar":
        return text
    return "\u202b" + _NUM_RUN.sub(lambda m: "\u2066" + m.group() + "\u2069", text) + "\u202c"


def _t(key, lang):
    return _bidi(t(key, lang), lang)


def _hover_style():
    return dict(
        bgcolor="#1b1530",
        bordercolor="#1b1530",
        font=dict(family=FONT_FAMILY, color="#fff", size=13),
        align="left",
    )


def _font(size=12, color=INK_3):
    return dict(family=FONT_FAMILY, size=size, color=color)


def make_hourly_story(df, lang="en", baseline=None, window=None, level=None):
    df = df.sort_values("hour").reset_index(drop=True)
    hours = [int(h) for h in df["hour"].tolist()]
    vol = df["total"].tolist()
    rate = df["fraud_rate"].tolist()

    if baseline is None:
        baseline = 100 * sum(df["fraud"]) / sum(vol) if "fraud" in df else sum(rate) / len(rate)
    threshold = level if level is not None else 2 * baseline
    peak_hour = hours[rate.index(max(rate))]
    window = tuple(window) if window else (peak_hour, peak_hour)
    window_label = f"{window[0]:02d}:00–{(window[1] + 1) % 24:02d}:00"

    labels = [f"{h:02d}:00" for h in hours]
    tx_lbl = _t("chart_transactions", lang)
    rate_lbl = _t("chart_rate_name", lang)
    baseline_name = _bidi(t("chart_baseline_name", lang).format(rate=f"{baseline:.1f}"), lang)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=vol,
        yaxis="y",
        name=_t("chart_vol_name", lang),
        marker=dict(color="#c4b2d9", line=dict(width=0), cornerradius=3),
        hovertemplate=f"{tx_lbl}: %{{y:,.0f}}<extra></extra>",
    ))

    above = [r >= threshold for r in rate]
    fig.add_trace(go.Scatter(
        x=labels,
        y=rate,
        yaxis="y2",
        mode="lines+markers",
        name=rate_lbl,
        line=dict(color=PRIMARY, width=2.5, shape="linear"),
        marker=dict(
            color=[RED if a else PRIMARY for a in above],
            size=[10 if a else 7 for a in above],
            line=dict(color="#fff", width=2),
        ),
        hovertemplate=f"{rate_lbl}: %{{y:.1f}}%<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None], yaxis="y2", mode="markers",
        name=_t("chart_above_name", lang),
        marker=dict(color=RED, size=10, line=dict(color="#fff", width=2)),
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], yaxis="y2", mode="lines",
        name=baseline_name,
        line=dict(color=INK_3, width=1.5, dash="dash"),
        hoverinfo="skip",
    ))

    x0 = window[0] - 0.5
    x1 = window[1] + 0.5
    fig.add_shape(
        type="rect", xref="x", yref="paper", x0=x0, x1=x1, y0=0, y1=1,
        fillcolor=RED, opacity=0.06, line_width=0, layer="below",
    )
    fig.add_shape(
        type="line", xref="paper", yref="y2", x0=0, x1=1, y0=baseline, y1=baseline,
        line=dict(color=INK_3, width=1.5, dash="dash"), layer="below",
    )

    fig.add_annotation(
        x=(x0 + x1) / 2, xref="x", y=1.0, yref="paper", yanchor="bottom",
        text=f"<b>{_bidi(t('chart_window', lang).format(label=window_label), lang)}</b>", showarrow=False, font=_font(12, RED),
    )
    peak_idx = rate.index(max(rate))
    fig.add_annotation(
        x=labels[peak_idx], y=rate[peak_idx], xref="x", yref="y2",
        text=f"<b>{rate[peak_idx]:.1f}%</b>", showarrow=False, yshift=18, font=_font(13, RED),
    )
    fig.add_annotation(
        x=1, xref="paper", xanchor="right", y=baseline, yref="y2", yshift=-12,
        text=baseline_name, showarrow=False, font=_font(11, INK_2),
    )

    tick_text = [
        f"<span style='color:{RED}'><b>{h:02d}</b></span>" if window[0] <= h <= window[1] else f"{h:02d}"
        for h in hours
    ]

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_font(12),
        margin=dict(l=70, r=16, t=64, b=56),
        hovermode="x unified",
        hoversubplots="axis",
        hoverlabel=_hover_style(),
        hoverdistance=-1,
        bargap=0.28,
        dragmode=False,
        legend=dict(
            orientation="h", xanchor="right", x=1, yanchor="bottom", y=1.06,
            font=_font(12, INK_2), bgcolor="rgba(0,0,0,0)", itemclick=False, itemdoubleclick=False,
        ),
        xaxis=dict(
            type="category",
            categoryorder="array",
            categoryarray=labels,
            anchor="y2",
            tickmode="array",
            tickvals=labels,
            ticktext=tick_text,
            tickfont=_font(11),
            title=dict(text=_t("chart_x_title", lang), font=_font(12), standoff=12),
            showgrid=False,
            fixedrange=True,
            showspikes=True,
            spikemode="across",
            spikesnap="data",
            spikethickness=1,
            spikedash="solid",
            spikecolor="#9aa0b4",
        ),
        yaxis=dict(
            domain=[0.56, 1.0],
            title=dict(text=_t("chart_vol_title", lang), font=_font(12), standoff=8),
            tickformat="~s",
            gridcolor=GRID,
            zeroline=False,
            fixedrange=True,
            tickfont=_font(11),
            rangemode="tozero",
        ),
        yaxis2=dict(
            domain=[0.0, 0.44],
            anchor="x",
            title=dict(text=_t("chart_rate_title", lang), font=_font(12), standoff=8),
            ticksuffix="%",
            gridcolor=GRID,
            zeroline=False,
            fixedrange=True,
            tickfont=_font(11),
            range=[0, max(rate) * 1.22],
        ),
    )
    return fig


def make_gauge(probability, lang="en", low_max=0.30, medium_max=0.60):
    pct = probability * 100
    lo = round(low_max * 100, 1)
    hi = round(max(medium_max, low_max + 0.05) * 100, 1)
    if pct > hi:
        bar_color = RED
    elif pct > lo:
        bar_color = "#d99a00"
    else:
        bar_color = "#1d7a3a"

    low_l, med_l, high_l = _t("gauge_low", lang), _t("gauge_medium", lang), _t("gauge_high", lang)
    ticks = [
        (0, "0"),
        (lo / 2, f"<span style='color:#1d7a3a'>{low_l}</span>") if lo >= 12 else None,
        (lo, f"{lo:g}"),
        ((lo + hi) / 2, f"<span style='color:#8a5a00'>{med_l}</span>") if hi - lo >= 12 else None,
        (hi, f"{hi:g}"),
        ((hi + 100) / 2, f"<span style='color:{RED}'>{high_l}</span>"),
        (100, "100"),
    ]
    ticks = [tk for tk in ticks if tk]
    tickvals = [v for v, _ in ticks]
    ticktext = [txt for _, txt in ticks]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number=dict(suffix="%", valueformat=".1f", font=dict(family=FONT_FAMILY, size=44, color=INK, weight=700)),
        domain=dict(x=[0, 1], y=[0, 1]),
        gauge=dict(
            shape="angular",
            axis=dict(
                range=[0, 100],
                tickmode="array",
                tickvals=tickvals,
                ticktext=ticktext,
                ticks="",
                tickfont=_font(12),
                showticklabels=True,
            ),
            bar=dict(color=bar_color, thickness=0.32),
            bgcolor="#ffffff",
            borderwidth=0,
            steps=[
                dict(range=[0, lo], color="#dff3e5"),
                dict(range=[lo, hi], color="#fcefcc"),
                dict(range=[hi, 100], color="#fbdcd9"),
            ],
            threshold=dict(line=dict(color=bar_color, width=4), thickness=0.9, value=pct),
        ),
    ))
    fig.update_layout(
        height=250,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=48, r=48, t=28, b=8),
        font=dict(family=FONT_FAMILY),
    )
    return fig


def make_confusion_matrix(metrics, lang="en"):
    tn, fp, fn, tp = metrics["tn"], metrics["fp"], metrics["fn"], metrics["tp"]
    total = tn + fp + fn + tp

    legit, fraud = _t("cm_legit", lang), _t("cm_fraud", lang)
    x_labels = [legit, fraud]
    y_labels = [legit, fraud]

    names = [["True Neg", "False Pos"], ["False Neg", "True Pos"]]
    values = [[tn, fp], [fn, tp]]
    shorts = [
        [_t("cm_tn_short", lang), _t("cm_fp_short", lang)],
        [_t("cm_fn_short", lang), _t("cm_tp_short", lang)],
    ]
    meanings = [
        [_t("cm_tn_res", lang), _t("cm_fp_res", lang)],
        [_t("cm_fn_res", lang), _t("cm_tp_res", lang)],
    ]
    correct = [[1, 0], [0, 1]]

    customdata = [
        [[names[i][j], f"{values[i][j]:,}", f"{100 * values[i][j] / total:.1f}%", meanings[i][j], y_labels[i], x_labels[j]]
         for j in range(2)]
        for i in range(2)
    ]

    ht = (
        "<b>%{customdata[0]}</b> · %{customdata[4]} → %{customdata[5]}<br>"
        f"{_t('cm_count', lang)}: %{{customdata[1]}}<br>"
        f"{_t('cm_share', lang)}: %{{customdata[2]}}<br>"
        "%{customdata[3]}<extra></extra>"
    )

    fig = go.Figure(go.Heatmap(
        z=correct,
        x=x_labels,
        y=y_labels,
        customdata=customdata,
        hovertemplate=ht,
        colorscale=[[0, "#fbd9d6"], [1, PRIMARY]],
        zmin=0,
        zmax=1,
        showscale=False,
        xgap=6,
        ygap=6,
    ))

    for i in range(2):
        for j in range(2):
            ok = correct[i][j] == 1
            main = "#ffffff" if ok else "#8f1d15"
            sub = "#d9d0e8" if ok else "#8f1d15"
            for text, size, color, shift, bold in (
                (names[i][j], 14, main, 26, False),
                (f"{values[i][j]:,}", 26, main, 0, True),
                (shorts[i][j], 13, sub, -26, False),
            ):
                fig.add_annotation(
                    x=x_labels[j], y=y_labels[i], showarrow=False, yshift=shift,
                    text=f"<b>{text}</b>" if bold else text,
                    font=dict(family=FONT_FAMILY, size=size, color=color),
                )

    fig.update_layout(
        height=370,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_font(13, INK_2),
        margin=dict(l=76, r=8, t=64, b=8),
        hoverlabel=_hover_style(),
        dragmode=False,
        xaxis=dict(
            side="top",
            title=dict(text=f"<b>{_t('cm_pred_axis', lang)}</b>", font=_font(13, INK_2), standoff=6),
            tickfont=_font(13, INK_2),
            showgrid=False, zeroline=False, fixedrange=True, ticks="",
        ),
        yaxis=dict(
            autorange="reversed",
            title=dict(text=f"<b>{_t('cm_actual_axis', lang)}</b>", font=_font(13, INK_2), standoff=6),
            tickfont=_font(13, INK_2),
            showgrid=False, zeroline=False, fixedrange=True, ticks="",
        ),
    )
    return fig


def make_feature_importance(df, lang="en", top_n=10):
    df = df.nlargest(top_n, "importance").sort_values("importance", ascending=True).reset_index(drop=True)
    features = df["feature"].tolist()
    importances = df["importance"].tolist()

    colors = ["#4a3470"] * len(features)
    if colors:
        colors[-1] = PRIMARY

    x_title = _t("fi_x_title", lang)
    fig = go.Figure(go.Bar(
        x=importances,
        y=features,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        hovertemplate=f"<b>%{{y}}</b><br>{x_title}: %{{x:.4f}}<extra></extra>",
    ))

    fig.update_layout(
        height=max(320, 40 * len(features) + 70),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_font(13),
        margin=dict(l=8, r=24, t=8, b=48),
        bargap=0.3,
        hoverlabel=_hover_style(),
        dragmode=False,
        xaxis=dict(
            title=dict(text=x_title, font=_font(12)),
            showgrid=True, gridcolor=GRID, fixedrange=True, zeroline=False, tickfont=_font(11),
        ),
        yaxis=dict(
            showgrid=False, fixedrange=True, automargin=True, ticks="", ticksuffix="  ",
            tickfont=_font(14, INK),
        ),
    )
    return fig
