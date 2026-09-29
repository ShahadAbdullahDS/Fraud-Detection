from html import escape

import streamlit as st


ICONS = {
    "shield": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/></svg>',
    "info": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></svg>',
    "check": '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>',
    "clock": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2d1b4e" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "mail": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2d1b4e" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "dollar": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2d1b4e" stroke-width="2" aria-hidden="true"><path d="M12 3v18M16.5 7.5c0-1.7-2-2.8-4.5-2.8S7.5 5.8 7.5 7.7c0 4.3 9 2.3 9 6.8 0 1.9-2 3-4.5 3s-4.5-1.2-4.5-3"/></svg>',
    "dot": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2d1b4e" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/></svg>',
    "warn": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17h.01"/></svg>',
    "ok": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>',
    "alert_wrong": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c8281e" stroke-width="2.2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5h.01"/></svg>',
    "alert_ok": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1d7a3a" stroke-width="2.4" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>',
}


def _html(markup):
    st.markdown(markup, unsafe_allow_html=True)


def attr(text):
    return escape(str(text), quote=True)


def info_dot(text, title=None):
    if not text:
        return ""
    head = f"<b>{escape(title)}</b>" if title else ""
    return (
        f'<span class="info-dot" tabindex="0" role="button" aria-label="{attr(title or "Info")}: {attr(text)}">i'
        f'<span class="tip" role="tooltip">{head}{escape(text)}</span></span>'
    )


def brand(subtitle):
    _html(
        f'<div class="fsd-brand"><div class="logo">{ICONS["shield"]}</div>'
        f'<div><b>Fraud Signal Desk</b><small>{escape(subtitle)}</small></div></div>'
    )


def page_heading(title, subtitle=None):
    sub = f'<div class="sub">{escape(subtitle)}</div>' if subtitle else ""
    _html(f'<div class="fsd-ph"><div class="h1" role="heading" aria-level="1">{escape(title)}</div>{sub}</div>')


def section_header_html(title, subtitle=None, info=None):
    sub = f'<div class="sub">{escape(subtitle)}</div>' if subtitle else ""
    return (
        f'<div class="fsd-sh"><div class="txt"><div class="h2" role="heading" aria-level="2">{escape(title)}</div>{sub}</div>'
        f'{info_dot(info, title)}</div>'
    )


def section_header(title, subtitle=None, info=None, info_key=None):
    _html(section_header_html(title, subtitle, info))


def metric_tile_html(label, value, tooltip):
    return (
        f'<div class="metric-tile tt" data-tip="{attr(tooltip)}" tabindex="0">'
        f'<div class="l">{escape(label)}</div><div class="v">{escape(value)}</div></div>'
    )


def metric_tile(label, value, tooltip=None):
    _html(metric_tile_html(label, value, tooltip or ""))


def metric_row(tiles):
    _html('<div class="metric-grid">' + "".join(metric_tile_html(*t) for t in tiles) + "</div>")


def kpi_card_html(label, value, description, highlight=False, tooltip=None):
    hl = " hl" if highlight else ""
    tip = f' tt" data-tip="{attr(tooltip)}' if tooltip else ""
    return (
        f'<div class="kpi-card{hl}{tip}" tabindex="0">'
        f'<div class="l">{escape(label)}</div><div class="v">{escape(value)}</div>'
        f'<div class="d">{escape(description)}</div></div>'
    )


def kpi_card(label, value, description, highlight=False, tooltip=None):
    _html(kpi_card_html(label, value, description, highlight, tooltip))


def kpi_grid(cards):
    _html('<div class="kpi-grid">' + "".join(kpi_card_html(**c) for c in cards) + "</div>")


def badge(text, kind="neutral", tooltip=None):
    cls = {"fraud": "b-fraud", "legit": "b-legit", "neutral": "b-neutral", "amber": "b-amber"}.get(kind, "b-neutral")
    tip = f' tt" data-tip="{attr(tooltip)}' if tooltip else ""
    return f'<span class="badge {cls}{tip}">{escape(text)}</span>'


def info_note(text):
    _html(f'<div class="info-note">{ICONS["info"]}<span>{escape(text)}</span></div>')


def empty_state(text):
    _html(f'<div class="empty-state">{escape(text)}</div>')


def step_header(number, title, right_text=None):
    rt = f'<span class="range">{escape(right_text)}</span>' if right_text else ""
    _html(
        f'<div class="fsd-step"><span class="n">{number}</span>'
        f'<div class="h2" role="heading" aria-level="2">{escape(title)}</div>{rt}</div>'
    )
