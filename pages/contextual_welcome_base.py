from __future__ import annotations
# pages/contextual_welcome_base.py - modal + pills + collage (no feature cards, no JS)
from pathlib import Path
import streamlit as st

# --- theme fallback (keeps app running even if theme import fails)
try:
    from ui.theme import inject_theme
except Exception:
    def inject_theme() -> None:
        st.markdown(
            """
            <style>
              .block-container{max-width:1160px;padding-top:8px;}
              header[data-testid="stHeader"]{background:transparent;}
              footer{visibility:hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

# Collage images already in static/images/
IMAGE_FOR = {
    "you": "static/images/contextual_welcome_self.png",
    "loved": "static/images/contextual_welcome_someone_else.png",
}

COPY = {
    "you": {
        "h1": "We're here to help you find the support you're looking for.",
        "ph": "What's your name?",
        "tip": "",
    },
    "loved": {
        "h1": "We're here to help you find the support your loved ones need.",
        "ph": "What's their name?",
        "tip": "If you want to assess several people, don't worry - you can easily move on to the next step!",
    },
}

def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()

def _inject_css(hero_url: str) -> None:
    st.markdown(
        f"""
        <style>
          :root {{
            --ink: #0f172a;
            --muted: #475569;
            --surface: #ffffff;
            --primary: #0b5cd8;
            --bg: #eaf1ff;
          }}
          body {{ background: var(--bg); }}
          .cw-hero {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background-image: url("{hero_url}");
            background-repeat: no-repeat;
            background-position: right 5% bottom 5%;
            background-size: contain;
            filter: drop-shadow(0 16px 30px rgba(2,8,23,.25));
          }}
          .cw-modal {{
            position: relative;
            z-index: 2;
            margin: 80px auto;
            width: 560px;
            max-width: 88vw;
            background: var(--surface);
            border-radius: 16px;
            box-shadow: 0 12px 30px rgba(2,8,23,.10);
            padding: 24px;
            text-align: center;
          }}
          .cw-h1 {{
            font-size: 1.55rem;
            line-height: 1.25;
            font-weight: 800;
            color: var(--ink);
            margin: 0 0 16px;
          }}
          .cw-tip {{
            margin-top: 12px;
            color: var(--muted);
            font-size: 0.9rem;
          }}
          .cw-pills {{
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 16px;
          }}
          .cw-pills button {{
            border-radius: 16px;
            padding: 8px 16px;
            border: 2px solid var(--primary);
            background: transparent;
            color: var(--ink);
          }}
          .cw-pills button[aria-pressed="true"] {{
            background: var(--primary);
            color: white;
          }}
          .cw-close {{
            position: absolute;
            top: 16px;
            right: 16px;
            font-size: 1.2rem;
            border: none;
            background: none;
            cursor: pointer;
          }}
          .cw-input-row {{
            display: flex;
            gap: 16px;
            justify-content: center;
          }}
          .cw-input-row input {{
            flex: 1;
            max-width: 300px;
          }}
          .cw-input-row button {{
            flex: 0 0 auto;
          }}
        </style>
        <div class="cw-hero"></div>
        """,
        unsafe_allow_html=True,
    )

def render(which: str = "you") -> None:
    """which ∈ {'you','loved'}"""
    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="wide")
    which = "you" if which not in ("you", "loved") else which
    st.session_state.setdefault("cw_which", which)
    
    # CSS + background collage
    hero = IMAGE_FOR[st.session_state["cw_which"]]
    _inject_css(hero)
    
    # Modal
    st.markdown('<div class="cw-modal">', unsafe_allow_html=True)
    
    # Close button
    st.markdown('<button class="cw-close" onclick="window.location.href=\'pages/hub.py\'">×</button>', unsafe_allow_html=True)
    
    # Pills
    st.markdown('<div class="cw-pills">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(
            "👥 For someone",
            key="cw_pill_loved",
            type="primary" if st.session_state["cw_which"] == "loved" else "secondary",
            use_container_width=True,
        ):
            st.session_state["cw_which"] = "loved"
            st.rerun()
    with col2:
        if st.button(
            "👤 For me",
            key="cw_pill_you",
            type="primary" if st.session_state["cw_which"] == "you" else "secondary",
            use_container_width=True,
        ):
            st.session_state["cw_which"] = "you"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Header
    copy = COPY["loved" if st.session_state["cw_which"] == "loved" else "you"]
    st.markdown(f'<div class="cw-h1">{copy["h1"]}</div>', unsafe_allow_html=True)
    
    # Input + Continue
    st.markdown('<div class="cw-input-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        name = st.text_input(copy["ph"], key="cw_name")
    with col2:
        if st.button("Continue", key="cw_go", use_container_width=True):
            people = st.session_state.setdefault("people", {"recipient_name": ""})
            people["recipient_name"] = name.strip()
            _safe_switch_page("pages/hub.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tip
    if copy["tip"]:
        st.markdown(f'<div class="cw-tip">{copy["tip"]}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)