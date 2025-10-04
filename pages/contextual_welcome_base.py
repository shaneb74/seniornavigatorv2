from __future__ import annotations
"""Shared renderer for the Contextual Welcome experience (modal + pills + collage)."""

import streamlit as st

# --- theme fallback (keeps app running even if theme import fails) ---
try:
    from ui.theme import inject_theme  # type: ignore
except Exception:  # pragma: no cover
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

# Optional: we only read the current role from audiencing if present
try:
    from audiencing import ensure_audiencing_state  # type: ignore
except Exception:  # pragma: no cover
    def ensure_audiencing_state():
        return {"entry": "proxy", "people": {"recipient_name": "", "proxy_name": ""}}

# Collage images that you already placed in static/images/
IMAGE_MAP = {
    "self": "static/images/contextual_welcome_self.png",
    "proxy": "static/images/contextual_welcome_someone_else.png",
}

COPY = {
    "self": {
        "headline": "We are here to help you find the support you are looking for.",
        "name_placeholder": "What is your name?",
        "pill_left": "For someone",
        "pill_right": "For me",
    },
    "proxy": {
        "headline": "We are here to help you find the support your loved ones need.",
        "name_placeholder": "What is their name?",
        "pill_left": "For someone",
        "pill_right": "For me",
    },
}

def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        # Fallback for older Streamlit
        st.query_params["next"] = target
        st.experimental_rerun()

def _inject_page_css() -> None:
    st.markdown(
        """
        <style>
          /* canvas */
          .cw-wrap{
            position:relative;
            min-height:86vh;
            background:var(--surface-subtle,#eef4ff);
            border-radius:18px;
            overflow:hidden;
          }
          /* collage on the right, behind the modal */
          .cw-collage{
            position:absolute;
            right:4%;
            top:8%;
            width:min(52vw,980px);
            max-width:980px;
            z-index:0;
            pointer-events:none;
            opacity:1;
          }
          .cw-collage img{
            width:100%;
            height:auto;
            display:block;
            object-fit:contain;
            filter:drop-shadow(0 18px 24px rgba(2,6,23,.18));
          }

          /* modal/card */
          .cw-card{
            position:relative;
            z-index:1;
            width:min(640px,92vw);
            background:#fff;
            border-radius:16px;
            padding:20px 22px 22px;
            margin:10vh 0 0 4vw;
            box-shadow:0 10px 30px rgba(2,6,23,.12);
          }

          /* pills row */
          .cw-pills{ display:flex; gap:12px; align-items:center; }
          .cw-pill{
            border:1px solid rgba(15,23,42,.12);
            background:#eef2ff;
            border-radius:12px;
            padding:10px 16px;
            font-weight:600;
            cursor:pointer;
            user-select:none;
          }
          .cw-pill.active{
            background:#0b5cd8;
            color:#fff;
            border-color:#0b5cd8;
          }
          .cw-x{
            margin-left:auto;
            border:1px solid rgba(15,23,42,.12);
            background:#fff;
            width:36px;height:36px;
            display:flex;align-items:center;justify-content:center;
            border-radius:10px;
            line-height:0; font-weight:700;
          }

          .cw-h1{
            margin:14px 2px 14px;
            font-size:28px; line-height:1.25; font-weight:800;
            color:var(--ink,#0f172a);
          }

          /* Streamlit widget tweaks inside the card */
          .cw-card [data-testid="stTextInput"] label{ display:none !important; }
          .cw-card [data-testid="stTextInput"] input{
            height:46px; border-radius:10px;
          }
          .cw-card .stButton>button{
            height:46px; border-radius:10px;
            font-weight:700;
          }
          .cw-helper{
            margin-top:6px;
            color:var(--ink-muted,#475569);
            font-size:.9rem;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render(which: str = "you") -> None:
    """Render the contextual welcome. `which` is 'you' or 'loved'."""
    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="wide")

    # entry key and copy
    entry = "self" if str(which).lower() in ("you", "self", "me") else "proxy"
    copy = COPY[entry]
    img_src = IMAGE_MAP.get(entry, "")

    # absorb existing state (not required, but safe)
    state = ensure_audiencing_state()
    people = state.setdefault("people", {"recipient_name": "", "proxy_name": ""})

    _inject_page_css()
    st.markdown('<div class="cw-wrap">', unsafe_allow_html=True)

    # collage
    if img_src:
        st.markdown(f'<div class="cw-collage"><img src="{img_src}" alt="collage"></div>', unsafe_allow_html=True)

    # modal card
    st.markdown('<div class="cw-card">', unsafe_allow_html=True)

    # pills row
    col_left, col_right, col_x = st.columns([1.05, 1.0, 0.2], gap="small")
    with col_left:
        if st.button(copy["pill_left"], key="cw_pill_left", use_container_width=True):
            _safe_switch_page("pages/contextual_welcome_loved_one.py")
        st.markdown(
            '<script>var b=document.querySelector("button[kind=cw_pill_left]");</script>',
            unsafe_allow_html=True,
        )
    with col_right:
        if st.button(copy["pill_right"], key="cw_pill_right", use_container_width=True):
            _safe_switch_page("pages/contextual_welcome_self.py")
    with col_x:
        st.button("x", key="cw_close", use_container_width=True)

    # mark active pill with CSS class via simple hint (works with our styles)
    active_left = entry == "proxy"
    active_right = entry == "self"
    st.markdown(
        f"""
        <script>
        const pills = Array.from(document.querySelectorAll('.stButton button'));
        if (pills.length >= 2) {{
          pills[0].classList.add('cw-pill', '{'active' if active_left else ''}');
          pills[1].classList.add('cw-pill', '{'active' if active_right else ''}');
        }}
        const closeBtn = document.querySelector('button[kind="cw_close"]');
        if (closeBtn) closeBtn.classList.add('cw-x');
        </script>
        """,
        unsafe_allow_html=True,
    )

    # headline
    st.markdown(f'<div class="cw-h1">{copy["headline"]}</div>', unsafe_allow_html=True)

    # name input
    name_placeholder = copy["name_placeholder"]
    name_key = "cw_name_self" if entry == "self" else "cw_name_proxy"
    name = st.text_input(name_placeholder, value="", key=name_key, label_visibility="collapsed")
    if entry == "self":
        people["proxy_name"] = ""
    else:
        people["recipient_name"] = name

    # Continue
    c1, c2 = st.columns([1, 1])
    with c2:
        if st.button("Continue", key="cw_continue", use_container_width=True):
            _safe_switch_page("pages/hub.py")

    st.caption(
        "If you want to assess several people, do not worry - you can easily move on to the next step!",
        help=None,
    )

    st.markdown("</div>", unsafe_allow_html=True)   # end .cw-card
    st.markdown("</div>", unsafe_allow_html=True)   # end .cw-wrap
