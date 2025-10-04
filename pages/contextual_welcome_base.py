from __future__ import annotations

from pathlib import Path
import streamlit as st

# --- theme fallback (keeps app running even if theme import fails) ---
try:
    from ui.theme import inject_theme
except Exception:
    def inject_theme() -> None:
        st.markdown(
            "<style>.block-container{max-width:1160px}footer{visibility:hidden}</style>",
            unsafe_allow_html=True,
        )

# --------- assets ----------
IMG = {
    "self":  "static/images/contextual_welcome_self.png",
    "proxy": "static/images/contextual_welcome_someone_else.png",
}

COPY = {
    "self": {
        "headline": "We are here to help you find the support you are looking for.",
        "placeholder": "What is your name?",
        "helper": "",
    },
    "proxy": {
        "headline": "We are here to help you find the support your loved ones need.",
        "placeholder": "What is their name?",
        "helper": "If you want to assess several people, do not worry - you can easily move on to the next step!",
    },
}

# --------- state helpers ----------
def _aud() -> dict:
    ss = st.session_state.setdefault("audiencing", {})
    ss.setdefault("entry", None)
    ss.setdefault("people", {"recipient_name": "", "proxy_name": ""})
    return ss

def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.rerun()

# --------- renderer ----------
def render(entry: str = "self") -> None:
    # allow synonyms from wrappers
    entry = {"you": "self", "self": "self", "loved": "proxy", "proxy": "proxy"}.get(entry, "self")

    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="wide")

    aud = _aud()
    aud["entry"] = entry  # remember selection

    # read current name
    people = aud["people"]
    if entry == "self":
        current_name = people.get("proxy_name", "")
    else:
        current_name = people.get("recipient_name", "")

    # ------------- CSS -------------
    st.markdown(
        """
        <style>
          :root{
            --ink:#0f172a; --ink-muted:#5b6a83; --cta:#0b5cd8; --card:#ffffff; --bg:#eef3ff;
          }
          body{ background:var(--bg)!important; }
          .cw-wrap{ position:relative; min-height:72vh; }
          .cw-card{
            width:560px; background:var(--card); border-radius:20px;
            box-shadow:0 16px 40px rgba(16,24,40,.16);
            padding:22px 22px 18px; position:relative; z-index:2;
          }
          .cw-close{
            position:absolute; right:16px; top:14px; width:28px; height:28px;
            border-radius:50%; border:1px solid #e5e7eb; display:grid; place-items:center;
            cursor:pointer; background:#fff; font-weight:700;
          }
          .cw-tabs{ display:flex; gap:10px; margin-bottom:12px; }
          .cw-tab{
            padding:8px 14px; border-radius:10px; border:1px solid #e5e7eb;
            font-weight:600; cursor:pointer; user-select:none;
          }
          .cw-tab.active{ background:#111827; color:#fff; border-color:#111827; }
          .cw-tab.alt{ background:#e9f2ff; color:#1f2937; border-color:#d6e6ff; }
          .cw-h1{ font-size:24px; font-weight:800; color:var(--ink); margin:6px 0 10px; }
          .cw-cap{ color:var(--ink-muted); font-size:14px; }
          .cw-row{ display:flex; gap:12px; margin-top:16px; align-items:center; }
          .cw-input input{
            width:100%; padding:12px 14px; border-radius:10px; border:1px solid #e5e7eb;
          }
          .cw-btn{
            padding:12px 18px; border-radius:10px; border:none; background:var(--cta); color:#fff;
            font-weight:700; cursor:pointer; width:100%;
          }
          .cw-hero{
            position:absolute; right:0; top:40px; width:min(56vw, 720px);
            z-index:1; transform:rotate(-1deg);
          }
          @media (max-width: 980px){
            .cw-card{ width:100%; }
            .cw-hero{ opacity:.15; width:80vw; right:-10vw; top:60px; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------- layout -------------
    st.markdown('<div class="cw-wrap">', unsafe_allow_html=True)

    # right composite image
    img_path = IMG[entry]
    if Path(img_path).exists():
        st.markdown(f'<img class="cw-hero" src="/{img_path}" alt="context image">', unsafe_allow_html=True)

    # the modal/card
    st.markdown('<div class="cw-card">', unsafe_allow_html=True)

    # close → Hub
    if st.button("×", key="cw_close", help="Close"):
        _safe_switch_page("pages/hub.py")
    st.markdown('<div class="cw-close" style="display:none"></div>', unsafe_allow_html=True)

    # tabs
    left, right = st.columns([1, 3])
    with left:
        st.markdown('<div class="cw-tabs">', unsafe_allow_html=True)
        if entry == "proxy":
            st.markdown('<div class="cw-tab alt">For someone</div>', unsafe_allow_html=True)
        else:
            if st.button("For someone", key="cw_tab_proxy"):
                _safe_switch_page("pages/contextual_welcome_loved_one.py")
        if entry == "self":
            st.markdown('<div class="cw-tab active">For me</div>', unsafe_allow_html=True)
        else:
            if st.button("For me", key="cw_tab_self"):
                _safe_switch_page("pages/contextual_welcome_self.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # headline
    st.markdown(f'<div class="cw-h1">{COPY[entry]["headline"]}</div>', unsafe_allow_html=True)

    # name + continue
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        name = st.text_input(COPY[entry]["placeholder"], value=current_name, key=f"cw_name_{entry}")
    with c2:
        if st.button("Continue", key=f"cw_go_{entry}", use_container_width=True):
            if entry == "self":
                people["proxy_name"] = name.strip()
            else:
                people["recipient_name"] = name.strip()
            _safe_switch_page("pages/hub.py")

    # helper (only for proxy)
    helper = COPY[entry]["helper"]
    if helper:
        st.markdown(f'<div class="cw-cap" style="margin-top:14px;">{helper}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)   # /.cw-card
    st.markdown('</div>', unsafe_allow_html=True)   # /.cw-wrap
