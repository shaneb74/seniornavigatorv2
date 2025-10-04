from __future__ import annotations
# pages/contextual_welcome_base.py - modal + pills + collage (no feature cards, no JS)

from pathlib import Path
import streamlit as st

# --- theme fallback (keeps app running even if theme import fails)
try:
    from ui.theme import inject_theme  # type: ignore
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
    "you":   "static/images/contextual_welcome_self.png",
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
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()

def _inject_css(hero_url: str) -> None:
    # NOTE: all CSS braces are doubled {{ }} because this is an f-string
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

          /* hero collage at right/bottom */
          .cw-hero {{
            position: fixed;
            right: min(2.5vw, 24px);
            bottom: min(2vh, 24px);
            width: min(62vw, 980px);
            z-index: 0;
            pointer-events: none;
            user-select: none;
          }}
          .cw-hero img {{
            width: 100%;
            height: auto;
            filter: drop-shadow(0 16px 30px rgba(2,8,23,.25));
            border: 0;
            display: block;
          }}

          /* modal */
          .cw-modal {{
            position: relative;
            z-index: 2;
            margin-left: min(6vw, 48px);
            margin-top: min(10vh, 80px);
            width: min(560px, 88vw);
            background: var(--surface);
            border-radius: 16px;
            box-shadow: 0 12px 30px rgba(2,8,23,.10);
            padding: 22px 22px 24px;
          }}
          .cw-h1 {{
            font-size: 1.55rem;
            line-height: 1.25;
            font-weight: 800;
            color: var(--ink);
            margin: 6px 0 16px;
          }}
          .cw-tip {{
            margin-top: 12px;
            color: var(--muted);
            font-size: .9rem;
          }}
        </style>
        <div class="cw-hero"><img src="{hero_url}" alt=""></div>
        """,
        unsafe_allow_html=True,
    )

def render(which: str = "you") -> None:
    """which ∈ {{'you','loved'}}"""
    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="wide")

    which = "you" if which not in ("you", "loved") else which
    st.session_state.setdefault("cw_which", which)

    # CSS + background collage
    hero = IMAGE_FOR[st.session_state["cw_which"]]
    _inject_css(hero)

    # Modal
    st.markdown('<div class="cw-modal">', unsafe_allow_html=True)

    # Header row: pills on left, close on right
    ph1, ph2 = st.columns([6, 1])
    with ph1:
        bcol1, bcol2 = st.columns([1, 1])
        with bcol1:
            if st.button(
                "👥 For someone",
                key="cw_pill_loved",
                type="primary" if st.session_state["cw_which"] == "loved" else "secondary",
                use_container_width=True,
            ):
                st.session_state["cw_which"] = "loved"
                st.rerun()
        with bcol2:
            if st.button(
                "👤 For me",
                key="cw_pill_you",
                type="primary" if st.session_state["cw_which"] == "you" else "secondary",
                use_container_width=True,
            ):
                st.session_state["cw_which"] = "you"
                st.rerun()
    with ph2:
        if st.button("×", key="cw_close", type="secondary"):
            _safe_switch_page("pages/hub.py")

    copy = COPY["loved" if st.session_state["cw_which"] == "loved" else "you"]
    st.markdown(f'<div class="cw-h1">{copy["h1"]}</div>', unsafe_allow_html=True)

    # Input + Continue
    c1, c2 = st.columns([3, 2])
    with c1:
        name = st.text_input(copy["ph"], key="cw_name")
    with c2:
        if st.button("Continue", key="cw_go", use_container_width=True):
            people = st.session_state.setdefault("people", {"recipient_name": ""})
            people["recipient_name"] = name.strip()
            _safe_switch_page("pages/hub.py")

    if copy["tip"]:
        st.markdown(f'<div class="cw-tip">{copy["tip"]}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
