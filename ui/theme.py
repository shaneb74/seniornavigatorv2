import streamlit as st
from pathlib import Path

TOKENS = {
    "brand": "#0B5CD8",
    "paper": "#ffffff",
    "surface": "#f6f8fa",
    "ink": "#111418",
    "ink-muted": "#6b7280",
    "radius": "16px",
}

def inject_theme() -> None:
    """Apply design tokens + optional repo CSS (static/style.css)."""

    # Core tokens and a couple of layout tweaks
    base_css = f"""
    <style>
      :root {{
        --brand: {TOKENS["brand"]};
        --paper: {TOKENS["paper"]};
        --surface: {TOKENS["surface"]};
        --ink: {TOKENS["ink"]};
        --ink-muted: {TOKENS["ink-muted"]};
        --radius: {TOKENS["radius"]};
      }}
      .block-container {{ max-width:1160px; padding-top:8px; }}
      header[data-testid="stHeader"] {{ background:transparent; }}
      footer {{ visibility:hidden; }}

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

    # Optional repo CSS (this is where your sidebar color etc. likely lived)
    extra = ""
    css_path = Path("static/style.css")
    if css_path.exists():
        try:
            extra = css_path.read_text(encoding="utf-8").strip()
        except Exception:
            extra = css_path.read_bytes().decode(errors="ignore").strip()

    # If you want the dark/brand sidebar back, keep these two rules here or in static/style.css
    sidebar_css = """
    <style>
      section[data-testid="stSidebar"] { background: var(--brand) !important; }
      section[data-testid="stSidebar"] * { color: white !important; }
    </style>
    """

    st.markdown(base_css, unsafe_allow_html=True)
    if extra:
        st.markdown(f"<style>{extra}</style>", unsafe_allow_html=True)
    # Comment this line if you move the sidebar rules into static/style.css
    st.markdown(sidebar_css, unsafe_allow_html=True)