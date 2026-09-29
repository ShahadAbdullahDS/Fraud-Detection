import streamlit as st

st.set_page_config(
    page_title="Fraud Signal Desk",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.config import t, DEFAULT_LANG
from ui.styles import inject_css
from ui.components import brand
from views.overview import render_overview
from views.model_analysis import render_model_analysis

if "lang" not in st.session_state:
    st.session_state["lang"] = DEFAULT_LANG
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "overview"
if "nav_seg" not in st.session_state:
    st.session_state["nav_seg"] = st.session_state["current_page"]
if "lang_seg" not in st.session_state:
    st.session_state["lang_seg"] = st.session_state["lang"]


def _on_nav():
    choice = st.session_state.get("nav_seg")
    if choice is None:
        st.session_state["nav_seg"] = st.session_state["current_page"]
        return
    if choice != st.session_state["current_page"]:
        st.session_state["current_page"] = choice
        st.session_state["analysis_done"] = False


def _on_lang():
    choice = st.session_state.get("lang_seg")
    if choice is None:
        st.session_state["lang_seg"] = st.session_state["lang"]
        return
    st.session_state["lang"] = choice


lang = st.session_state["lang"]
inject_css(lang)

with st.container(key="topbar"):
    top_cols = st.columns([4, 5, 2], vertical_alignment="center")
    with top_cols[0]:
        brand(t("app_subtitle", lang))
    with top_cols[1]:
        pages = {"overview": t("page_overview", lang), "model": t("page_model", lang)}
        st.segmented_control(
            "nav",
            options=list(pages.keys()),
            format_func=lambda k: pages[k],
            label_visibility="collapsed",
            key="nav_seg",
            on_change=_on_nav,
        )
    with top_cols[2]:
        langs = {"en": "English", "ar": "العربية"}
        st.segmented_control(
            "lang",
            options=list(langs.keys()),
            format_func=lambda k: langs[k],
            label_visibility="collapsed",
            key="lang_seg",
            on_change=_on_lang,
        )

if st.session_state["current_page"] == "overview":
    render_overview(lang)
else:
    render_model_analysis(lang)
