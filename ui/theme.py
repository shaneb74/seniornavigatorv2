import streamlit as st

TOKENS = {
    "brand": "#0B5CD8",
    "paper": "#ffffff",
    "surface": "#f6f8fa",
    "ink": "#111418",
    "ink-muted": "#6b7280",
    "radius": "16px",
}

def inject_theme() -> None:
    css = f"""
    <style>
      :root {{
        --brand: {TOKENS["brand"]};
        --paper: {TOKENS["paper"]};
        --surface: {TOKENS["surface"]};
        --ink: {TOKENS["ink"]};
        --ink-muted: {TOKENS["ink-muted"]};
        --radius: {TOKENS["radius"]};
      }}
      .block-container {{max-width:1160px; padding-top:8px;}}
      header[data-testid="stHeader"] {{background:transparent;}}
      footer {{visibility:hidden;}}

      /* Cards & notes used by PFMA/CP drawers */
      .sn-card, .pfma-card {{
        background: var(--surface);
        border: 1px solid rgba(0,0,0,.08);
        border-radius: var(--radius);
        padding: clamp(1rem, 2vw, 1.5rem);
      }}
      .pfma-note {{
        font-size:.9rem; color:var(--ink-muted);
        margin:.25rem 0 0 0;
      }}
      .sn-hero h1, .pfma-header h1 {{
        font-size: clamp(1.6rem, 3.2vw, 2.2rem);
        margin: 0 0 .25rem 0;
      }}
      .sn-hero p, .pfma-header p {{ color: var(--ink-muted); margin: 0; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
