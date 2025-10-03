from __future__ import annotations

# ui/theme.py
# Design tokens + global CSS. Exposes BOTH inject() and inject_theme().
import streamlit as st

TOKENS = {
    "brand": "#0B5CD8",
    "brand_ink": "#ffffff",
    "ink": "#0f172a",
    "muted": "#475569",
    "muted_soft": "#64748b",
    "chip": "#E6EEFF",
    "chip_border": "#C7D2FE",
    "chip_ink": "#1E3A8A",
    "card": "#ffffff",
    "bg": "#F8FAFC",
    "radius": "16px",
    "radius_lg": "24px",
    "ring": "rgba(11,92,216,.18)",
    "shadow_1": "0 8px 24px rgba(15, 23, 42, 0.06)",
    "shadow_2": "0 24px 60px -30px rgba(15, 23, 42, 0.35)",
    "success": "#16a34a",
}

CSS = f"""
<style>
:root {{
  --brand:{TOKENS['brand']};
  --brand-ink:{TOKENS['brand_ink']};
  --ink:{TOKENS['ink']};
  --ink-soft:{TOKENS['muted']};
  --ink-muted:{TOKENS['muted_soft']};
  --chip:{TOKENS['chip']};
  --chip-border:{TOKENS['chip_border']};
  --chip-ink:{TOKENS['chip_ink']};
  --card:{TOKENS['card']};
  --bg:{TOKENS['bg']};
  --radius:{TOKENS['radius']};
  --radius-lg:{TOKENS['radius_lg']};
  --ring:{TOKENS['ring']};
  --shadow-1:{TOKENS['shadow_1']};
  --shadow-2:{TOKENS['shadow_2']};
  --success:{TOKENS['success']};
  --focus-ring:0 0 0 4px {TOKENS['ring']};
  --border:#d7dce6;
  --border-strong:#b8c3d9;
  --bg-soft:#f1f5f9;

  /* legacy aliases */
  --sn-primary: var(--brand);
  --sn-primary-dark:#094bb6;
  --sn-primary-soft: rgba(11, 92, 216, 0.12);
  --sn-success: var(--success);
  --sn-text: var(--ink);
  --sn-text-muted: var(--ink-muted);
  --sn-bg: var(--bg);
  --sn-card: var(--card);
  --sn-border: var(--border);
  --sn-border-strong: var(--border-strong);
  --sn-shadow: var(--shadow-2);
  --sn-radius: var(--radius);
  --sn-radius-lg: var(--radius-lg);
  --sn-chip-bg: var(--chip);
  --sn-chip-text: var(--chip-ink);
  --sn-helper-bg: rgba(11, 92, 216, 0.08);
  --sn-helper-border: rgba(11, 92, 216, 0.18);
}}

body,
.stApp,
[data-testid="stAppViewContainer"] {{
  font-family: "Inter", "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--ink);
}}

.stApp {{
  font-size: 17px;
  line-height: 1.55;
}}

[data-testid="stAppViewContainer"] > .main {{
  padding-top: 2.6rem;
  padding-bottom: 4.5rem;
}}

.block-container {{
  max-width: 1160px;
  margin: 0 auto;
  background: transparent;
  border-radius: var(--radius-lg);
  padding: clamp(2rem, 4vw, 3rem);
}}

header[data-testid="stHeader"] {{
  background: transparent;
}}

footer {{
  visibility: hidden;
}}

a,
[data-testid="stMarkdownContainer"] a {{
  color: var(--brand);
  text-decoration: none;
  font-weight: 600;
}}

a:hover,
[data-testid="stMarkdownContainer"] a:hover {{
  text-decoration: underline;
}}

/* Typography helpers */
.sn-hero-h1{{ font-size: clamp(28px, 4.2vw, 44px); line-height:1.05; font-weight:800; letter-spacing:.015em; margin:0 0 .4rem; color:var(--ink); }}
.sn-hero-h2{{ font-size: clamp(18px, 2.2vw, 20px); color: var(--ink-muted); font-weight:500; margin:.4rem 0 1.1rem; }}
.sn-field-note {{ margin-top:.6rem; color: var(--ink-muted); font-size:.96rem; }}
.sn-helper-note {{ background:var(--sn-helper-bg); border:1px solid var(--sn-helper-border); border-radius: var(--radius); padding: .9rem 1.1rem; color:var(--ink); margin-top:1.1rem; font-size: .98rem; }}
.sn-hr{{ height:1px; background:#e5e7eb; border-radius:1px; margin: 18px 0 12px; }}

/* Grid + card primitives */
.sn-grid {{ display:grid; gap:18px; width:100%; }}
.sn-grid.two {{ grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}

.sn-card,
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-1);
  padding: 1.4rem 1.6rem;
}}

.sn-card--gradient {{
  background: radial-gradient(120% 120% at 85% 10%, rgba(255, 232, 232, 0.45) 0%, rgba(255,255,255,0) 42%),
              radial-gradient(120% 120% at 12% 92%, rgba(238, 246, 255, 0.8) 0%, rgba(255,255,255,0) 48%),
              var(--card);
}}

.sn-card h3 {{ margin:0 0 6px; font-size:1.18rem; font-weight:750; color:var(--ink); }}
.sn-card p {{ margin:4px 0 12px; color:var(--ink-muted); font-size:.98rem; }}

.sn-field-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-1);
  padding: 1.15rem 1.2rem;
  height: 100%;
}}

.sn-field-hint {{ color: var(--ink-muted); margin-top: .45rem; font-size:.94rem; }}

.sn-badge {{
  display:inline-flex; align-items:center; gap:.35rem;
  font-size:.78rem; padding:.32rem .62rem; border-radius:999px;
  background: var(--chip); color: var(--chip-ink); border:1px solid var(--chip-border);
}}

.sn-chip {{
  display:inline-flex; align-items:center; gap:.35rem;
  padding:.38rem .72rem; border-radius:999px;
  background:#f1f5f9; color:var(--ink); border:1px solid #d7dee9; font-weight:600; font-size:.88rem;
}}

.sn-chip.active {{ background:var(--ink); color:white; border-color:var(--ink); }}

.sn-notice {{
  display:flex; align-items:center; gap:.6rem;
  background:#eef6ff; color:#0b3e91; border:1px solid #cfe4ff;
  padding:.625rem .9rem; border-radius:10px; font-size:.92rem; margin: 6px 0 18px;
}}

.sn-banner {{
  display:flex; gap:.75rem; align-items:flex-start;
  background:#f8fbff; border:1px solid var(--border);
  border-radius: var(--radius);
  padding: .95rem 1.1rem;
  color: var(--ink);
  box-shadow: var(--shadow-1);
}}

.sn-banner--success {{ border-color: rgba(22,163,74,.25); background: rgba(22,163,74,.08); color: var(--success); }}

/* Buttons */
.sn-btn {{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:.45rem;
  font-weight:700;
  font-size:.95rem;
  padding:.62rem 1.05rem;
  border-radius:999px;
  border:1px solid var(--border);
  background:#f8fbff;
  color:#0b3e91;
  transition: all .18s ease;
  text-decoration:none;
}}

.sn-btn.primary {{
  background: var(--brand);
  color: var(--brand-ink);
  border-color: transparent;
}}

.sn-btn:hover {{
  box-shadow: 0 0 0 4px var(--ring);
  transform: translateY(-1px);
  color:#0b3e91;
}}

.sn-btn.primary:hover {{
  background: #0a4fc0;
  color: var(--brand-ink);
}}

.stButton > button,
button[kind] {{
  border-radius: 999px !important;
  padding: 0.78rem 1.85rem !important;
  font-weight: 700 !important;
  border: 1px solid transparent !important;
  box-shadow: none !important;
  transition: background .18s ease, color .18s ease, transform .18s ease;
}}

button[kind="primary"],
.stButton > button:not([kind]) {{
  background: var(--brand) !important;
  color: var(--brand-ink) !important;
}}

button[kind="primary"]:hover,
.stButton > button:not([kind]):hover {{
  background: #0a4fc0 !important;
  transform: translateY(-1px);
}}

button[kind="secondary"],
.stButton > button[kind="secondary"] {{
  background: transparent !important;
  border-color: var(--border) !important;
  color: var(--ink) !important;
}}

.stButton > button:focus,
button[kind]:focus {{
  outline: none !important;
  box-shadow: var(--focus-ring) !important;
}}

/* Segmented radios + choice groups */
.sn-segmented div[role="radiogroup"],
.sn-choice-group div[role="radiogroup"] {{
  display: inline-flex;
  gap: .6rem;
  flex-wrap: wrap;
}}

.sn-segmented label,
.sn-choice-group label {{
  border-radius: 999px !important;
  border:1px solid var(--border) !important;
  padding: .55rem 1.4rem !important;
  background: white;
  color: var(--ink-muted);
  font-weight: 600;
}}

.sn-choice-group label {{ border-radius: var(--radius) !important; padding: .75rem 1.1rem !important; }}

.sn-segmented label[data-baseweb="radio"]:hover,
.sn-choice-group label[data-baseweb="radio"]:hover {{
  border-color: var(--brand);
  color: var(--ink);
}}

.sn-segmented label[data-baseweb="radio"][aria-checked="true"],
.sn-choice-group label[data-baseweb="radio"][aria-checked="true"] {{
  background: var(--brand);
  border-color: var(--brand);
  color: var(--brand-ink);
}}

.sn-choice-note {{ margin-top:.45rem; color: var(--ink-muted); font-size:.95rem; }}

/* Sticky footer */
.sn-sticky-footer {{
  position: sticky;
  bottom: 0;
  padding: 1rem 0 0;
  margin-top: 2.4rem;
  background: linear-gradient(180deg, rgba(248,250,252,0) 0%, rgba(248,250,252,0.92) 38%, rgba(248,250,252,1) 100%);
  backdrop-filter: blur(10px);
}}

.sn-sticky-footer .sn-footer-inner {{
  display:flex;
  gap: 1rem;
  align-items:center;
  justify-content:center;
}}

.sn-footer-note {{
  margin-top:.65rem;
  text-align:center;
  color: var(--ink-muted);
  font-size:.92rem;
}}

/* Dashboard helpers */
.sn-dashboard-grid {{
  display:grid;
  gap:18px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}}

.sn-dashboard-card {{
  background: var(--card);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-1);
  padding: 1.4rem 1.5rem;
  display:flex;
  flex-direction:column;
  gap:1.05rem;
}}

.sn-dashboard-note {{
  display:flex; gap:.5rem; align-items:center; margin-top:16px;
}}

.sn-dashboard-note button {{
  background: transparent !important;
  border: none !important;
  color: var(--brand) !important;
  padding: 0 !important;
}}

.sn-compact-row {{
  display:grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap:14px;
  margin-top:14px;
}}

.sn-compact-tile {{
  background: var(--card);
  border:1px solid var(--border);
  border-radius:14px;
  padding: 1rem 1.1rem;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
}}

.sn-compact-tile .title {{ font-weight:700; color:var(--ink); }}
.sn-compact-tile .subtitle {{ color: var(--ink-muted); font-size:.94rem; margin-top:.2rem; }}

/* Inline inputs */
.sn-inline-input {{
  display:flex;
  gap:.9rem;
  align-items:flex-end;
  flex-wrap:wrap;
}}

.sn-inline-input .sn-inline-field {{ flex: 1 1 220px; }}
.sn-inline-input .sn-inline-cta {{ flex: 0 0 auto; }}

/* Guided Care Plan */
.sn-gcp-stepper {{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
  margin-bottom: 1.2rem;
}}

.sn-gcp-stepper .sn-gcp-progress {{
  flex:1;
  height: 6px;
  background:#e2e8f0;
  border-radius:999px;
  position:relative;
}}

.sn-gcp-stepper .sn-gcp-progress::after {{
  content:"";
  position:absolute;
  inset:0;
  width: var(--sn-step-progress, 0%);
  background: var(--brand);
  border-radius:999px;
}}

.sn-gcp-steps {{
  display:flex;
  gap:.75rem;
  font-size:.9rem;
  color: var(--ink-muted);
}}

.sn-gcp-steps .sn-step-active {{ color: var(--brand); font-weight:700; }}

/* Debug blocks */
.sn-debug {{
  background:#0f172a;
  color:#e2e8f0;
  padding:1rem 1.2rem;
  border-radius: var(--radius);
  font-family: "JetBrains Mono", monospace;
  font-size:.85rem;
}}

/* Streamlit native adjustments */
[data-testid="stNotification"] {{
  border-radius: var(--radius);
  border:1px solid var(--border);
}}

[data-testid="stImage"] img {{
  border-radius: var(--radius);
}}

/* Toggle focus visibility */
[data-testid="stToggle"] label:focus-visible {{
  outline: none;
  box-shadow: var(--focus-ring);
  border-radius: 12px;
}}

/* =========================
   Button normalization block
   =========================
   Force all Streamlit buttons to use theme tokens, even if a page injects later CSS.
*/
.stButton > button,
button[kind],
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
[data-testid="stFormSubmitButton"] > button,
a[kind="primary"] > button,
a[data-testid="stLinkButton"] > button {{
  background: var(--brand) !important;
  color: var(--brand-ink) !important;
  border: 1px solid transparent !important;
  border-radius: 999px !important;
  padding: 0.78rem 1.85rem !important;
  font-weight: 700 !important;
  box-shadow: none !important;
}}

.stButton > button:hover,
button[kind]:hover,
[data-testid="stFormSubmitButton"] > button:hover,
a[data-testid="stLinkButton"] > button:hover {{
  background: #0a4fc0 !important;
  color: var(--brand-ink) !important;
  transform: translateY(-1px);
}}

button[kind="secondary"],
.stButton > button[kind="secondary"] {{
  background: transparent !important;
  color: var(--ink) !important;
  border: 1px solid var(--border) !important;
}}

button:disabled {{
  opacity: .55 !important;
  cursor: not-allowed !important;
}}

/* Kill any leftover "danger" variants painting things red */
.sn-btn.danger,
.stButton .danger,
button.danger {{
  background: var(--brand) !important;
  color: var(--brand-ink) !important;
  border-color: transparent !important;
}}

/* Extra coverage for Streamlit submit buttons */
div[data-testid="stFormSubmitButton"] > button,
div[data-testid="formSubmitButton"] > button,
form button[type="submit"],
form [data-testid="baseButton-primary"] > button,
form [data-testid="baseButton-secondary"] > button {{
  background: var(--brand) !important;
  color: var(--brand-ink) !important;
  border: 1px solid transparent !important;
  border-radius: 999px !important;
  padding: 0.78rem 1.85rem !important;
  font-weight: 700 !important;
  box-shadow: none !important;
}}

div[data-testid="stFormSubmitButton"] > button:hover,
div[data-testid="formSubmitButton"] > button:hover,
form button[type="submit"]:hover,
form [data-testid="baseButton-primary"] > button:hover,
form [data-testid="baseButton-secondary"] > button:hover {{
  background: #0a4fc0 !important;
  color: var(--brand-ink) !important;
  transform: translateY(-1px);
}}

/* =========================
   Scoped button variants
   ========================= */

/* DASHBOARD scope: strong brand blue + white text */
.sn-scope.dashboard .stButton > button,
.sn-scope.dashboard [data-testid="stFormSubmitButton"] > button {{
  background: var(--brand) !important;
  color: var(--brand-ink) !important;
  border: 1px solid transparent !important;
  border-radius: 999px !important;
  padding: 0.78rem 1.85rem !important;
  font-weight: 700 !important;
}}
.sn-scope.dashboard .stButton > button:hover,
.sn-scope.dashboard [data-testid="stFormSubmitButton"] > button:hover {{
  background: #0a4fc0 !important;
  transform: translateY(-1px);
}}

/* Optional dashboard outline variant */
.sn-scope.dashboard .sn-btn--outline .stButton > button,
.sn-scope.dashboard .sn-btn--outline [data-testid="stFormSubmitButton"] > button {{
  background: transparent !important;
  color: var(--ink) !important;
  border: 1px solid var(--border) !important;
}}

/* GCP/Q&A scope: light blue pill + dark text */
.sn-scope.gcp .stButton > button,
.sn-scope.gcp [data-testid="stFormSubmitButton"] > button {{
  background: var(--chip) !important;
  color: var(--chip-ink) !important;
  border: 1px solid var(--chip-border) !important;
  border-radius: 14px !important;
  padding: 0.86rem 1.6rem !important;
  font-weight: 700 !important;
}}
.sn-scope.gcp .stButton > button:hover,
.sn-scope.gcp [data-testid="stFormSubmitButton"] > button:hover {{
  background: #dbe6ff !important;
  transform: translateY(-1px);
}}

/* GCP "Skip" (subtle) */
.sn-scope.gcp .sn-btn--subtle .stButton > button,
.sn-scope.gcp .sn-btn--subtle [data-testid="stFormSubmitButton"] > button {{
  background: #f1f5f9 !important;
  color: var(--ink) !important;
  border: 1px solid #d7dee9 !important;
}}

</style>
"""

def _already_injected() -> bool:
    return "_sn_theme_injected" in st.session_state

def _mark_injected() -> None:
    st.session_state["_sn_theme_injected"] = True

def inject_theme() -> None:
    """Primary API expected by app.py"""
    if not _already_injected():
        st.markdown(CSS, unsafe_allow_html=True)
        _mark_injected()

def inject() -> None:
    """Alias kept for older imports."""
    inject_theme()

# ----- Scoped container helper
from contextlib import contextmanager

@contextmanager
def scope(kind: str):
    """
    Wrap a section so scoped CSS applies:
      with scope("dashboard"): ...
      with scope("gcp"): ...
    """
    st.markdown(f'<div class="sn-scope {kind}">', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)