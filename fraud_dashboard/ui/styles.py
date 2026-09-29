import streamlit as st


def _css(lang):
    is_ar = lang == "ar"
    font_stack = (
        '"Tajawal", "Saira", system-ui, sans-serif'
        if is_ar else
        '"Saira", "Tajawal", system-ui, sans-serif'
    )
    ar_rules = """
    [data-testid="stMainBlockContainer"] .stMarkdown :is(div, span, b, em, p) { unicode-bidi: plaintext; }
    [data-testid="stMainBlockContainer"] .stMarkdown { text-align: left; }
    .fsd-ph, .fsd-headline, .fsd-sh .txt, .fsd-step { direction: rtl; text-align: right; }
    """ if is_ar else ""

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Saira:wght@400;500;600;700&family=Tajawal:wght@400;500;700&display=swap');
:root {{
  --primary:#2d1b4e; --primary-2:#4a3470; --lav:#c4b2d9; --lav-soft:#efe9f6;
  --bg:#f7f8fb; --surface:#ffffff; --border:#e3e5ec; --border-strong:#cfd3dd;
  --ink:#1b1530; --ink-2:#4b5064; --ink-3:#6b7084;
  --red:#c8281e; --red-bg:#fdecea; --red-soft:#fbd9d6;
  --green:#1d7a3a; --green-bg:#e8f5ec;
  --amber:#8a5a00; --amber-bg:#fdf3dc;
  --shadow-hover:0 2px 8px rgba(20,16,40,.06);
  --font:{font_stack};
}}
header[data-testid="stHeader"], footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="collapsedControl"], section[data-testid="stSidebar"] {{ display:none !important; }}
html, body, .stApp {{ background:var(--bg); }}
.stApp, .stApp :is(p, div, span, label, button, input, summary, b, em, small, h1, h2, h3) {{ font-family:var(--font); }}
.stApp [data-testid="stIconMaterial"], .stApp .material-symbols-rounded {{ font-family:"Material Symbols Rounded" !important; }}
[data-testid="stMainBlockContainer"] {{ max-width:1240px; padding:0 32px 56px !important; }}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {{ gap:24px; }}
.stElementContainer:has(> .stMarkdown style) {{ display:none; }}
.stMarkdown p {{ margin:0; }}
[data-testid="stMarkdownContainer"] {{ color:var(--ink); font-size:15px; line-height:1.5; margin-bottom:0 !important; }}
.stButton [data-testid="stMarkdownContainer"], [data-testid="stButtonGroup"] [data-testid="stMarkdownContainer"], .stTooltipContent [data-testid="stMarkdownContainer"] {{ color:inherit; }}

.st-key-topbar {{ padding:14px 0 12px; border-bottom:1px solid var(--border); gap:0; }}
.st-key-topbar [data-testid="stHorizontalBlock"] {{ align-items:center; }}
.fsd-brand {{ display:flex; align-items:center; gap:12px; }}
.fsd-brand .logo {{ width:36px; height:36px; border-radius:9px; background:var(--primary); display:grid; place-items:center; flex:none; }}
.fsd-brand b {{ display:block; font-size:17px; font-weight:700; line-height:1.15; color:var(--ink); }}
.fsd-brand small {{ display:block; font-size:13px; color:var(--ink-3); line-height:1.3; }}

.st-key-nav_seg [data-testid="stButtonGroup"] > div {{ gap:4px; border:0; background:transparent; }}
.st-key-nav_seg button {{
  background:transparent !important; border:0 !important; border-radius:0 !important; box-shadow:none !important;
  border-bottom:3px solid transparent !important; padding:10px 16px !important; min-height:0 !important;
  color:var(--ink-2) !important; cursor:pointer; transition:color 150ms ease, border-color 150ms ease;
}}
.st-key-nav_seg button p {{ font-size:15px !important; font-weight:500; color:inherit !important; }}
.st-key-nav_seg button:hover {{ color:var(--primary) !important; border-bottom-color:var(--border-strong) !important; }}
.st-key-nav_seg button[aria-checked="true"] {{ color:var(--primary) !important; border-bottom-color:var(--primary) !important; }}
.st-key-nav_seg button[aria-checked="true"] p {{ font-weight:600; }}
.st-key-nav_seg button:focus-visible {{ outline:3px solid rgba(45,27,78,.35) !important; outline-offset:2px; }}

.st-key-lang_seg {{ margin-left:auto; }}
.st-key-lang_seg [data-testid="stButtonGroup"] > div {{ background:#eef0f4; border-radius:8px; padding:3px; gap:0; border:0; }}
.st-key-lang_seg button {{
  background:transparent !important; border:0 !important; border-radius:6px !important; box-shadow:none !important;
  padding:5px 14px !important; min-height:0 !important; color:var(--ink-2) !important; cursor:pointer;
  transition:background 150ms ease, color 150ms ease;
}}
.st-key-lang_seg button p {{ font-size:14px !important; font-weight:500; color:inherit !important; }}
.st-key-lang_seg button:hover {{ color:var(--primary) !important; }}
.st-key-lang_seg button[aria-checked="true"] {{ background:var(--surface) !important; color:var(--primary) !important; box-shadow:0 1px 2px rgba(20,16,40,.12) !important; }}
.st-key-lang_seg button[aria-checked="true"] p {{ font-weight:600; }}
.st-key-lang_seg button:focus-visible {{ outline:3px solid rgba(45,27,78,.35) !important; outline-offset:2px; }}

.fsd-ph {{ padding-top:8px; }}
.fsd-ph .h1 {{ font-size:28px; font-weight:700; line-height:1.2; letter-spacing:-.01em; color:var(--ink); }}
.fsd-ph .sub {{ color:var(--ink-2); font-size:16px; margin-top:6px; }}

[class*="st-key-sec_"] {{
  background:var(--surface); border:1px solid var(--border) !important; border-radius:12px !important;
  padding:24px !important; gap:16px; transition:box-shadow 150ms ease;
}}
[class*="st-key-sec_"]:hover {{ box-shadow:var(--shadow-hover); }}

.fsd-sh {{ display:flex; align-items:flex-start; gap:10px; }}
.fsd-sh .txt {{ flex:1; min-width:0; }}
.fsd-sh .h2 {{ font-size:19px; font-weight:600; line-height:1.3; color:var(--ink); }}
.fsd-sh .sub {{ color:var(--ink-2); font-size:14px; margin-top:2px; }}

.info-dot {{
  position:relative; flex:none; width:26px; height:26px; border-radius:50%;
  border:1px solid var(--border-strong); background:var(--surface); color:var(--ink-2);
  display:inline-grid; place-items:center; font-size:13px; font-weight:600; line-height:1;
  cursor:help; transition:border-color 150ms ease, color 150ms ease, background 150ms ease; outline:none;
}}
.info-dot:hover, .info-dot:focus-visible {{ border-color:var(--primary); color:var(--primary); background:var(--lav-soft); }}
.info-dot:focus-visible {{ box-shadow:0 0 0 3px rgba(45,27,78,.25); }}
.info-dot .tip {{
  position:absolute; top:calc(100% + 8px); right:0; z-index:1000;
  width:max-content; max-width:300px; padding:10px 12px; border-radius:8px;
  background:#1b1530; color:#fff; box-shadow:0 6px 16px rgba(0,0,0,.18);
  font-size:13px; font-weight:400; line-height:1.5; text-align:start; unicode-bidi:plaintext;
  opacity:0; visibility:hidden; transform:translateY(-4px); pointer-events:none;
  transition:opacity 150ms ease, transform 150ms ease, visibility 150ms;
}}
.info-dot .tip b {{ display:block; font-weight:600; margin-bottom:4px; color:#fff; }}
.info-dot:hover .tip, .info-dot:focus-visible .tip {{ opacity:1; visibility:visible; transform:none; }}

.tt {{ position:relative; }}
.tt::after {{
  content:attr(data-tip); position:absolute; left:50%; bottom:calc(100% + 8px);
  transform:translate(-50%, 4px); background:#1b1530; color:#fff; font-size:13px; font-weight:400;
  line-height:1.4; padding:8px 10px; border-radius:8px; width:max-content; max-width:260px; z-index:1000;
  box-shadow:0 4px 12px rgba(0,0,0,.15); white-space:normal; text-align:start; unicode-bidi:plaintext;
  opacity:0; visibility:hidden; pointer-events:none; transition:opacity 150ms ease, transform 150ms ease, visibility 150ms;
}}
.tt:hover::after {{ opacity:1; visibility:visible; transform:translate(-50%, 0); }}

.metric-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:16px; }}
.metric-tile {{ border:1px solid var(--border); border-radius:10px; padding:18px 20px; background:var(--surface); cursor:help; transition:border-color 150ms ease, box-shadow 150ms ease; }}
.metric-tile:hover {{ border-color:var(--border-strong); box-shadow:var(--shadow-hover); }}
.metric-tile .l {{ font-size:14px; color:var(--ink-2); font-weight:500; }}
.metric-tile .v {{ font-size:36px; font-weight:700; line-height:1.1; margin-top:6px; color:var(--primary); font-variant-numeric:tabular-nums; }}

.kpi-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); grid-auto-rows:1fr; gap:16px; }}
.kpi-card {{ background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; min-height:140px; cursor:help; transition:border-color 150ms ease, box-shadow 150ms ease; }}
.kpi-card:hover {{ border-color:var(--border-strong); box-shadow:var(--shadow-hover); }}
.kpi-card .l {{ font-size:14px; color:var(--ink-2); font-weight:500; }}
.kpi-card .v {{ font-size:28px; font-weight:700; line-height:1.15; margin:6px 0 8px; color:var(--ink); font-variant-numeric:tabular-nums; }}
.kpi-card.hl .v {{ color:var(--red); }}
.kpi-card .d {{ font-size:14px; color:var(--ink-3); line-height:1.45; }}

.fsd-headline {{ margin-top:4px; display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; }}
.fsd-headline .n {{ font-size:28px; font-weight:700; color:var(--red); line-height:1; font-variant-numeric:tabular-nums; }}
.fsd-headline .t {{ font-size:15px; color:var(--ink-2); }}

.cm-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.cm-item {{ border:1px solid var(--border); border-radius:10px; padding:14px 16px; display:flex; gap:12px; background:var(--surface); transition:border-color 150ms ease, box-shadow 150ms ease; }}
.cm-item:hover {{ border-color:var(--primary); box-shadow:var(--shadow-hover); }}
.cm-item .sw {{ width:14px; height:14px; border-radius:4px; flex:none; margin-top:4px; }}
.cm-item b {{ display:block; font-size:15px; font-weight:600; color:var(--ink); }}
.cm-item .q {{ display:block; margin-top:2px; font-size:14px; color:var(--ink-2); }}
.cm-item em {{ font-style:normal; font-weight:600; color:var(--ink); }}
.cm-item .res {{ display:block; margin-top:8px; font-size:14px; font-weight:600; }}
.cm-item .res.ok {{ color:var(--green); }}
.cm-item .res.bad {{ color:var(--red); }}

.st-key-adv_exp [data-testid="stExpander"] details {{ background:var(--surface); border:1px solid var(--border); border-radius:12px; }}
.st-key-adv_exp [data-testid="stExpander"] summary {{ padding:18px 24px; }}
.st-key-adv_exp [data-testid="stExpander"] summary p {{ font-size:17px; font-weight:600; color:var(--ink); }}
.st-key-adv_exp [data-testid="stExpander"] summary:hover p {{ color:var(--primary); }}
.st-key-adv_exp [data-testid="stExpanderDetails"] {{ padding:0 24px 24px; }}
.fsd-cap {{ color:var(--ink-3); font-size:14px; }}

.info-note {{ background:var(--lav-soft); color:var(--primary); border-radius:8px; padding:10px 14px; font-size:14px; display:flex; gap:10px; align-items:center; }}
.info-note svg {{ flex:none; }}
.info-note span {{ color:var(--primary); }}

.badge {{ display:inline-flex; align-items:center; gap:4px; font-size:12px; font-weight:600; padding:3px 10px; border-radius:999px; white-space:nowrap; line-height:1.4; }}
.b-fraud {{ background:var(--red-bg); color:var(--red); }}
.b-legit {{ background:var(--green-bg); color:var(--green); }}
.b-neutral {{ background:#eef0f4; color:var(--ink-2); }}
.b-amber {{ background:var(--amber-bg); color:var(--amber); }}

.stButton > button {{
  border-radius:10px !important; cursor:pointer !important; min-height:40px;
  transition:background 150ms ease, border-color 150ms ease, color 150ms ease, box-shadow 150ms ease;
}}
.stButton > button p {{ font-weight:600; font-size:14px; }}
.stButton > button[kind="primary"] {{ background:var(--primary) !important; color:#fff !important; border:1px solid var(--primary) !important; }}
.stButton > button[kind="primary"]:hover:not(:disabled) {{ background:#3b2663 !important; border-color:#3b2663 !important; }}
.stButton > button[kind="secondary"] {{ background:var(--surface) !important; color:var(--ink) !important; border:1px solid var(--border-strong) !important; }}
.stButton > button[kind="secondary"]:hover:not(:disabled) {{ background:var(--lav-soft) !important; color:var(--primary) !important; border-color:var(--primary) !important; }}
.stButton > button:disabled {{ opacity:.4 !important; cursor:not-allowed !important; }}
.stButton > button:focus-visible {{ outline:3px solid rgba(45,27,78,.35) !important; outline-offset:2px !important; box-shadow:none !important; }}

.fsd-step {{ display:flex; align-items:center; gap:10px; }}
.fsd-step .n {{ width:26px; height:26px; border-radius:50%; background:var(--primary); color:#fff; font-size:13px; font-weight:600; display:grid; place-items:center; flex:none; }}
.fsd-step h2, .fsd-step .h2 {{ font-size:19px; font-weight:600; margin:0; color:var(--ink); }}
.fsd-step .range {{ color:var(--ink-2); font-size:14px; margin-inline-start:auto; }}

.st-key-carousel [data-testid="stHorizontalBlock"] {{ align-items:center; }}
.st-key-arrow_prev .stButton, .st-key-arrow_next .stButton {{ display:flex; justify-content:center; }}
.st-key-arrow_prev .stButton > button, .st-key-arrow_next .stButton > button {{
  width:40px !important; height:40px !important; min-height:40px !important; border-radius:50% !important; padding:0 !important;
}}
.st-key-arrow_prev .stButton > button p, .st-key-arrow_next .stButton > button p {{ font-size:22px; line-height:1; margin-top:-3px; }}

[class*="st-key-card_"] {{
  background:var(--surface); border:1px solid var(--border) !important; border-radius:12px !important;
  padding:14px 14px 12px !important; gap:12px; transition:border-color 150ms ease, box-shadow 150ms ease;
}}
[class*="st-key-card_"]:hover {{ border-color:var(--border-strong) !important; box-shadow:var(--shadow-hover); }}
.sample .top {{ display:flex; justify-content:space-between; align-items:center; font-size:13px; color:var(--ink-3); font-weight:500; min-height:20px; }}
.sample .chk {{ width:20px; height:20px; border-radius:50%; background:var(--primary); display:grid; place-items:center; flex:none; }}
.sample .amt {{ font-size:22px; font-weight:700; margin:4px 0 0; color:var(--ink); font-variant-numeric:tabular-nums; }}
.sample .rows {{ margin-top:10px; border-top:1px solid var(--border); padding-top:10px; display:grid; gap:6px; }}
.sample .row {{ display:flex; justify-content:space-between; align-items:center; gap:8px; font-size:13px; }}
.sample .row span {{ color:var(--ink-3); white-space:nowrap; }}
.sample .row b {{ color:var(--ink); font-weight:600; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-variant-numeric:tabular-nums; }}

.st-key-car_foot [data-testid="stHorizontalBlock"] {{ align-items:center; }}
.dots {{ display:flex; gap:6px; align-items:center; font-size:13px; color:var(--ink-3); }}
.dots i {{ display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--border-strong); transition:width 150ms ease; }}
.dots i.on {{ background:var(--primary); width:22px; border-radius:4px; }}
.dots span {{ margin-left:8px; }}
.st-key-btn_analyze_wrap .stButton > button {{ min-height:44px; }}
.st-key-btn_analyze_wrap .stButton > button p {{ font-size:15px; }}

.details {{ display:grid; grid-template-columns:repeat(var(--n, 8), minmax(0,1fr)); border:1px solid var(--border); border-radius:10px; overflow:hidden; }}
.details > div {{ padding:14px 16px; border-left:1px solid var(--border); min-width:0; }}
.details > div:first-child {{ border-left:0; }}
.details span {{ display:block; font-size:13px; color:var(--ink-3); font-weight:500; }}
.details b {{ display:block; font-size:17px; font-weight:600; margin-top:2px; color:var(--ink); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-variant-numeric:tabular-nums; }}
@media (max-width:1100px) {{
  .details {{ grid-template-columns:repeat(3, minmax(0,1fr)); }}
  .details > div:nth-child(3n+1) {{ border-left:0; }}
  .details > div:nth-child(n+4) {{ border-top:1px solid var(--border); }}
}}

.verdict-wrap {{ text-align:center; }}
.verdict {{ display:inline-flex; align-items:center; gap:8px; font-weight:600; padding:6px 14px; border-radius:999px; font-size:15px; }}
.verdict.high {{ background:var(--red-bg); color:var(--red); }}
.verdict.medium {{ background:var(--amber-bg); color:var(--amber); }}
.verdict.low {{ background:var(--green-bg); color:var(--green); }}
.gauge-caption {{ font-size:14px; color:var(--ink-3); margin-top:10px; text-align:center; }}

.cues {{ display:grid; gap:12px; }}
.cue {{ border:1px solid var(--border); border-radius:10px; padding:14px 16px; display:grid; grid-template-columns:36px minmax(0,1fr) auto; gap:12px; align-items:center; transition:border-color 150ms ease, box-shadow 150ms ease; }}
.cue:hover {{ border-color:var(--border-strong); box-shadow:var(--shadow-hover); }}
.cue .ic {{ width:36px; height:36px; border-radius:9px; display:grid; place-items:center; background:var(--lav-soft); }}
.cue .k {{ font-size:13px; color:var(--ink-3); font-weight:500; }}
.cue .v {{ font-size:17px; font-weight:600; line-height:1.3; color:var(--ink); }}
.cue .ex {{ font-size:14px; color:var(--ink-2); margin-top:2px; }}

.alert {{ display:flex; gap:16px; align-items:flex-start; border-radius:12px; padding:20px 24px; }}
.alert.wrong {{ background:var(--red-bg); border:1px solid var(--red-soft); }}
.alert.correct {{ background:var(--green-bg); border:1px solid #bfe4c8; }}
.alert .ai {{ width:40px; height:40px; border-radius:50%; background:#fff; display:grid; place-items:center; flex:none; }}
.alert .body {{ flex:1; min-width:0; }}
.alert .h3 {{ font-size:17px; font-weight:600; display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
.alert.wrong .h3 {{ color:var(--red); }}
.alert.correct .h3 {{ color:var(--green); }}
.alert .cmp {{ display:grid; grid-template-columns:auto auto; gap:6px 24px; margin-top:10px; font-size:15px; width:max-content; align-items:center; }}
.alert .cmp > span {{ color:var(--ink-2); }}
.alert .cmp .badge {{ background:#fff; border:1px solid var(--border); }}
.alert .foot {{ margin-top:10px; font-size:14px; color:var(--ink-2); }}

.empty-state {{ background:var(--surface); border:1px dashed var(--border-strong); border-radius:12px; padding:40px 24px; text-align:center; color:var(--ink-3); font-size:15px; }}

[data-testid="stPlotlyChart"] {{ overflow:visible; }}
.stSpinner p {{ color:var(--ink-2); }}

@media (max-width:900px) {{
  .metric-grid, .kpi-grid {{ grid-template-columns:1fr; grid-auto-rows:auto; }}
  .cm-grid {{ grid-template-columns:1fr; }}
}}
{ar_rules}
</style>
"""


def inject_css(lang="en"):
    st.markdown(_css(lang), unsafe_allow_html=True)


def inject_rules(rules):
    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)
