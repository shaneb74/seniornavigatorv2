import streamlit as st

THEME_CSS = r"""
:root{
  /* Brand palette */
  --brand-600:#0B5CD8;   /* primary */
  --brand-700:#0A50BF;   /* hover/active */
  --brand-ring:#3B82F6;  /* focus ring */
  --on-brand:#FFFFFF;

  /* Disabled token that still keeps contrast on white text */
  --brand-600-disabled:#96B8F5;
}

/* ===== Primary Buttons — cover ALL Streamlit variants with high specificity ===== */

/* New buttons (baseButton) */
:where([data-testid="baseButton-primary"].st-emotion-cache-ue6h4q),
:where([data-testid="baseButton-primary"]),
/* Legacy buttons (kind="primary") */
:where(.stButton > button[kind="primary"]),
/* Link buttons set as primary */
:where(a[data-testid="stLinkButton"][data-variant="primary"]) {
  background-color: var(--brand-600) !important;
  color: var(--on-brand) !important;
  border: 1px solid var(--brand-600) !important;
  box-shadow: none !important;
}

/* Hover / active */
:where([data-testid="baseButton-primary"]:hover,
       .stButton > button[kind="primary"]:hover,
       a[data-testid="stLinkButton"][data-variant="primary"]:hover),
:where([data-testid="baseButton-primary"]:active,
       .stButton > button[kind="primary"]:active,
       a[data-testid="stLinkButton"][data-variant="primary"]:active){
  background-color: var(--brand-700) !important;
  border-color: var(--brand-700) !important;
  color: var(--on-brand) !important;
}

/* Focus-visible ring */
:where([data-testid="baseButton-primary"]:focus-visible,
       .stButton > button[kind="primary"]:focus-visible,
       a[data-testid="stLinkButton"][data-variant="primary"]:focus-visible){
  outline: 3px solid var(--brand-ring) !important;
  outline-offset: 2px !important;
}

/* Disabled state: keep white text for contrast */
:where([data-testid="baseButton-primary"][disabled],
       .stButton > button[kind="primary"][disabled],
       a[data-testid="stLinkButton"][data-variant="primary"][aria-disabled="true"]){
  background-color: var(--brand-600-disabled) !important;
  border-color: var(--brand-600-disabled) !important;
  color: var(--on-brand) !important;
  opacity: 1 !important; /* avoid ghosting */
  cursor: not-allowed !important;
}

/* Make sure any residual inline color doesn’t override us */
:where([data-testid="baseButton-primary"] *,
       .stButton > button[kind="primary"] *,
       a[data-testid="stLinkButton"][data-variant="primary"] *){
  color: var(--on-brand) !important;
}

/* ===== Hub tile primary button normalization (in case it renders as secondary) ===== */
.sn-tile .stButton > button,
.sn-tile [data-testid="baseButton-primary"]{
  background-color: var(--brand-600) !important;
  color: var(--on-brand) !important;
  border: 1px solid var(--brand-600) !important;
}

/* ===== Radio groups → pill buttons (robust against hydration) ===== */
/* Target Streamlit's stable structure/ARIA, not ephemeral class names */
:where([data-testid="stRadio"]) { --pill-bg:#ffffff; --pill-text:#111827; --pill-border:#e5e7eb;
                                    --pill-bg-selected:var(--brand-600); --pill-text-selected:#ffffff;
                                    --pill-border-selected:var(--brand-600); --pill-bg-hover:#f3f4f6; }

/* Layout & reset */
:where([data-testid="stRadio"] > div){ display:flex; flex-wrap:wrap; gap:.5rem; }
:where([data-testid="stRadio"] [role="radiogroup"]){ display:flex; flex-wrap:wrap; gap:.5rem; }

/* Hide native dots and make each option look like a pill */
:where([data-testid="stRadio"] [role="radio"]){
  position:relative;
  appearance:none !important;
  -webkit-appearance:none !important;
  border:1px solid var(--pill-border) !important;
  background:var(--pill-bg) !important;
  color:var(--pill-text) !important;
  border-radius:9999px !important;
  padding:.55rem .9rem !important;
  line-height:1 !important;
  cursor:pointer !important;
  box-shadow:none !important;
  outline:none !important;
  transition:background-color .12s ease,border-color .12s ease, color .12s ease !important;
}

/* Hover (mouse) */
:where([data-testid="stRadio"] [role="radio"]:hover){
  background:var(--pill-bg-hover) !important;
  border-color:#e5e7eb !important;
}

/* Selected state */
:where([data-testid="stRadio"] [role="radio"][aria-checked="true"]){
  background:var(--pill-bg-selected) !important;
  border-color:var(--pill-border-selected) !important;
  color:var(--pill-text-selected) !important;
}
:where([data-testid="stRadio"] [role="radio"][aria-checked="true"] *){
  color:var(--pill-text-selected) !important;
}

/* Keyboard focus ring (selected or not) */
:where([data-testid="stRadio"] [role="radio"]:focus-visible){
  outline:3px solid var(--brand-ring) !important;
  outline-offset:2px !important;
}

/* Kill any built-in pseudo bullets some themes add */
:where([data-testid="stRadio"] [role="radio"])::before,
:where([data-testid="stRadio"] [role="radio"])::after){
  content:none !important;
}

/* Ensure long labels wrap nicely as chips */
@media (max-width: 720px){
  :where([data-testid="stRadio"] > div, [data-testid="stRadio"] [role="radiogroup"]){
    gap:.45rem;
  }
}

/* Ensure pill text always inherits the correct color */
:where([data-testid="stRadio"] [role="radio"] * ) {
  color: inherit !important;
}

/* ===== Segmented Control (native pill group) ===== */
[data-testid="stSegmentedControl"] { --seg-gap: 8px; }
[data-testid="stSegmentedControl"] [role="tablist"] {
  display: flex; flex-wrap: wrap; gap: var(--seg-gap);
}
[data-testid="stSegmentedControl"] button[role="tab"] {
  border-radius: 9999px !important;
  border: 1px solid #E5E7EB !important;           /* light border */
  background: #FFFFFF !important;
  color: #111827 !important;
  padding: 8px 14px !important;
  line-height: 1.15 !important;
  transition: background-color .15s ease, border-color .15s ease;
}
[data-testid="stSegmentedControl"] button[role="tab"][aria-selected="true"] {
  background: var(--brand-600) !important;
  border-color: var(--brand-600) !important;
  color: var(--on-brand) !important;              /* white text on brand */
}
[data-testid="stSegmentedControl"] button[role="tab"]:hover {
  border-color: var(--brand-600) !important;
  background: #EEF2FF !important;                 /* subtle tint on hover */
}
[data-testid="stSegmentedControl"] button[role="tab"]:focus-visible {
  outline: 3px solid var(--brand-ring) !important;
  outline-offset: 2px !important;
}


"""


_THEME_FLAG = "_sn_theme_injected_v2"


def inject_theme() -> None:
    """Inject global CSS once per session, safely."""
    if st.session_state.get(_THEME_FLAG):
        return
    st.session_state[_THEME_FLAG] = True
    st.markdown(f"<style>{THEME_CSS}</style>", unsafe_allow_html=True)
