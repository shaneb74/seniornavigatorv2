from __future__ import annotations
"""Shared renderer for the Contextual Welcome experience (modal + pills + collage)."""

import base64, mimetypes
from pathlib import Path
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
            
@media (min-height: 900px){
  .cw-wrap{ padding:clamp(4px,1.5vh,12px) clamp(8px,2vw,16px); min-height:64vh; }
  .cw-card{ margin:clamp(8px,5vh,80px) 0 0 min(3vw, 24px); }
  .cw-collage{ top:2%; right:0.5%; width:min(580px, 54%); }
}

        </style>
            """,
            unsafe_allow_html=True,
        )

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

# Relationship choices (shown when entry == 'proxy')
RELATIONSHIP_CHOICES = [
    ("parent", "Parent"),
    ("spouse", "Spouse/Partner"),
    ("child", "Adult Child"),
    ("sibling", "Sibling"),
    ("relative", "Other Relative"),
    ("friend", "Friend/Neighbor"),
    ("caregiver", "Professional Caregiver"),
    ("poa_cm", "POA / Case Manager"),
    ("other", "Other"),
    ("unknown", "Prefer not to say"),
]

# ------------------ utilities ------------------
def _data_uri(path_str: str) -> str | None:
    """Read local image bytes and return a base64 data URI (safe for raw HTML)."""
    try:
        p = Path(path_str)
        if not p.exists():
            return None
        b = p.read_bytes()
        ext = p.suffix.lower()
        mime = mimetypes.types_map.get(ext, "image/png")
        return f"data:{mime};base64,{base64.b64encode(b).decode('ascii')}"
    except Exception:
        return None

def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()

def _inject_page_css() -> None:
    st.markdown(
        """
        <style>
          /* canvas */

          /* Shrink Streamlit canvas to content on THIS page only */
          section.main > div.block-container{
            min-height: auto !important;
            display: block !important;
            padding-top: 10px !important;
            padding-bottom: 14px !important;
          }
          /* Remove excess spacing on first/last vertical blocks */
          section.main > div.block-container [data-testid="stVerticalBlock"]{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
          }
          section.main > div.block-container > div:first-child{
            margin-top: 0 !important;
            padding-top: 0 !important;
          }
          /* Hide any accidental empty spacer blocks */
          section.main > div.block-container > div:empty{
            display:none !important;
          }
/* tighten Streamlit content pane (the big white rounded container) */
          .block-container{
            padding-top: 6px !important;
            padding-bottom: 12px !important;
            min-height: auto !important;
          }
          section.main > div.block-container{ min-height: auto !important; }
          [data-testid="stVerticalBlock"]{ padding-top: 0 !important; padding-bottom: 0 !important; }

          .cw-wrap{ padding:clamp(4px,1.5vh,12px) clamp(8px,2vw,16px);
            position:relative;
            min-height:auto;
            background:transparent;
            border-radius:18px;
            overflow:visible;
          }

          /* collage on the right, behind the modal */
          .cw-collage{
            position:absolute;
            right:1%;
            top:4%;
            width:min(600px, 56%);
            transform:rotate(-4deg);
            z-index:1; /* behind the card */
            opacity:.98;
            filter:drop-shadow(0 22px 40px rgba(0,0,0,.18));
          }
          .cw-collage img{
            width:100%;
            height:auto;
            border-radius:12px;
            display:block;
          }

          /* modal card */
          .cw-card{
            position:relative;
            z-index:10;         /* above collage */
            isolation:isolate;  /* new stacking context */
            background:#fff;
            margin:clamp(4px,2vh,28px) 0 0 min(3vw, 24px);
            padding: 20px 20px 14px;
            width:min(520px, 92vw);
            border-radius:14px;
            box-shadow:0 24px 60px rgba(2,12,27,.18);
          }

          .cw-card h2{
            margin:.2rem 0 .8rem 0;
            font-size:1.6rem;
            line-height:1.25;
          }

          /* pills row */
          .cw-card .pill-row{
            display:flex; gap:10px; margin:12px 0 16px;
          }
          .cw-card .pill-row .stButton>button{
            height:36px; border-radius:999px; padding:6px 16px; font-weight:700;
            width:auto !important;  /* prevent full-width pills */
          }

          /* inputs and CTA */
          .cw-card .stTextInput>div>div>input{
            height:44px; border-radius:10px;
          }
          .cw-card .cta{
            display:flex; justify-content:center; margin-top:8px;
          }
          .cw-card .cta .stButton>button{
            height:46px; border-radius:10px; font-weight:700; min-width:220px;
          }

          .cw-helper{
            margin-top:6px;
            color:var(--ink-muted,#475569);
            font-size:.9rem;
          }
        
@media (min-height: 900px){
  .cw-wrap{ padding:clamp(4px,1.5vh,12px) clamp(8px,2vw,16px); min-height:64vh; }
  .cw-card{ margin:clamp(8px,5vh,80px) 0 0 min(3vw, 24px); }
  .cw-collage{ top:2%; right:0.5%; width:min(580px, 54%); }
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

    # --- unify with session state used elsewhere (welcome.py) ---
    if "aud" not in st.session_state:
        st.session_state.aud = {
            "entry": entry,
            "recipient_name": None,
            "proxy_name": None,
            "relationship_code": None,
            "relationship_label": None,
            "relationship_other": None,
            "qualifiers": {},
        }
    aud = st.session_state.aud
    aud["entry"] = entry  # keep in sync

    _inject_page_css()
    st.markdown('<div class="cw-wrap">', unsafe_allow_html=True)

    # collage
    if img_src and not img_src.startswith(("http://", "https://", "data:")):
        img_src = _data_uri(img_src) or ""
    if img_src:
        st.markdown(f'<div class="cw-collage"><img src="{img_src}" alt="collage"></div>', unsafe_allow_html=True)

    # modal card
    st.markdown('<div class="cw-card">', unsafe_allow_html=True)

    # pills row (non-stretched)
    st.markdown('<div class="pill-row">', unsafe_allow_html=True)
    col_left, col_right, col_x = st.columns([1, 1, 0.2])
    with col_left:
        if st.button(copy["pill_left"], key="cw_pill_left", use_container_width=False):
            _safe_switch_page("pages/contextual_welcome_loved_one.py")
    with col_right:
        if st.button(copy["pill_right"], key="cw_pill_right", use_container_width=False):
            _safe_switch_page("pages/contextual_welcome_self.py")
    with col_x:
        st.button("x", key="cw_close", use_container_width=False, type="secondary")
    st.markdown('</div>', unsafe_allow_html=True)

    # headline
    st.markdown(f"<h2>{copy['headline']}</h2>", unsafe_allow_html=True)

    # name input
    name_placeholder = copy["name_placeholder"]
    name_key = "cw_name_self" if entry == "self" else "cw_name_proxy"
    name = st.text_input(name_placeholder, value=(aud.get("recipient_name") or ""), key=name_key, label_visibility="collapsed").strip()

    # persist aud fields
    if entry == "self":
        aud["recipient_name"] = name or aud.get("recipient_name")
        aud["proxy_name"] = None
    else:
        aud["recipient_name"] = name or aud.get("recipient_name")
        # Relationship select (proxy only, progressive reveal after name entered)
        if name:
            labels = [label for _, label in RELATIONSHIP_CHOICES]
            default_idx = labels.index(aud["relationship_label"]) if aud.get("relationship_label") in labels else 0
            rel_label = st.selectbox(
                f"What's your relationship to {name or 'them'}?",
                labels,
                index=default_idx,
                key="cw_relationship",
            )
            code_lookup = {label: code for code, label in RELATIONSHIP_CHOICES}
            aud["relationship_label"] = rel_label
            aud["relationship_code"] = code_lookup.get(rel_label)
            if aud["relationship_code"] == "other":
                aud["relationship_other"] = st.text_input(
                    "Briefly describe the relationship",
                    value=aud.get("relationship_other") or "",
                    key="cw_relationship_other",
                    label_visibility="collapsed",
                )
            else:
                aud["relationship_other"] = None
        else:
            # Clear relationship if the name is empty again
            aud["relationship_label"] = None
            aud["relationship_code"] = None
            aud["relationship_other"] = None

    # Continue - centered CTA
    name_ok = bool((aud.get("recipient_name") or "").strip())
    rel_ok = True if entry == "self" else bool(aud.get("relationship_code"))
    can_continue = name_ok and rel_ok

    st.markdown('<div class="cta">', unsafe_allow_html=True)
    if st.button("Continue", key="cw_continue", use_container_width=False, disabled=not can_continue):
        if not aud.get("recipient_name"):
            aud["recipient_name"] = "You" if entry == "self" else "Your Loved One"
        _safe_switch_page("pages/hub.py")
    st.markdown('</div>', unsafe_allow_html=True)

    if not name_ok:
        st.caption("Please enter a name to continue.", help=None)
    elif entry == "proxy" and not rel_ok:
        st.caption("Select your relationship to continue.", help=None)

    st.caption(
        "If you want to assess several people, do not worry - you can easily move on to the next step!",
        help=None,
    )

    st.markdown("</div>", unsafe_allow_html=True)   # end .cw-card
    st.markdown("</div>", unsafe_allow_html=True)   # end .cw-wrap
