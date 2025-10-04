from __future__ import annotations

# Contextual Welcome: shared renderer used by the "self" and "loved one" wrappers

from pathlib import Path
import streamlit as st

# --- theme fallback (keeps app running even if theme import fails) ---
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
              :root{
                --ink:#0f172a;
                --ink-muted:#5b6577;
                --surface:#ffffff;
                --pill:#f1f5ff;
                --pill-active:#0b5cd8;
                --pill-ink:#1e293b;
                --shadow:0 10px 30px rgba(2,6,23,.10), 0 2px 8px rgba(2,6,23,.06);
                --radius:18px;
              }
            </style>
            """,
            unsafe_allow_html=True,
        )

# --- small helpers -------------------------------------------------------

def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        try:
            st.query_params["next"] = target  # type: ignore[attr-defined]
        except Exception:
            pass
        # back-compat alias for older Streamlit
        if not hasattr(st, "rerun"):
            st.rerun = getattr(st, "experimental_rerun")  # type: ignore[attr-defined]
        st.rerun()

def _exists(p: str) -> bool:
    try:
        return Path(p).exists()
    except Exception:
        return False

# file paths and copy
IMAGE_FOR = {
    "you": "static/images/contextual_welcome_self.png",
    "loved": "static/images/contextual_welcome_someone_else.png",
}
HEADLINE = {
    "you": "We are here to help you find the support you are looking for.",
    "loved": "We are here to help you find the support your loved ones need.",
}
NAME_LABEL = {
    "you": "What is your name?",
    "loved": "What is their name?",
}
PILL = {
    "you": ("For someone", "For me"),
    "loved": ("For someone", "For me"),
}
# small explainer under the CTA (from the comp)
FOOTNOTE = (
    "If you want to assess several people, do not worry "
    "you can easily move on to the next step!"
)

# --- main render ---------------------------------------------------------

def render(key: str) -> None:
    """
    key: "you" or "loved"
    """

    # guard / defaults
    key = "you" if key not in ("you", "loved") else key

    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="wide")

    # page chrome / gradient bg
    st.markdown(
        """
        <style>
          body { background: #f3f6ff; }
          .cw-wrap{ position: relative; min-height: 72vh; }
          .cw-row{ display: grid; grid-template-columns: 520px 1fr; gap: 24px; align-items: center; }
          @media (max-width: 1100px){
            .cw-row{ grid-template-columns: 1fr; }
          }
          .cw-card{
            background: var(--surface);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 20px 22px;
            color: var(--ink);
          }
          .cw-pillbar{ display:inline-flex; gap:10px; margin-bottom:14px; }
          .cw-pill{
            font-size:.95rem; line-height:1; padding:9px 14px; border-radius:12px;
            background: var(--pill); color: var(--pill-ink);
            border:1px solid rgba(2,6,23,.06);
          }
          .cw-pill.active{
            background: var(--pill-active); color:#fff; border-color: var(--pill-active);
          }
          .cw-close{
            position:absolute; right:14px; top:14px; width:30px; height:30px;
            border-radius:999px; border:1px solid rgba(2,6,23,.08);
            display:grid; place-items:center; color:var(--ink-muted); background:#fff;
          }
          .cw-head{ font-size: 28px; font-weight:700; margin: 6px 0 2px 0; }
          .cw-sub{ color: var(--ink-muted); margin:0 0 12px 0; }
          .cw-grid3{ display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin: 10px 0 18px 0;}
          .cw-feature{ border:1px solid rgba(2,6,23,.08); border-radius: 12px; padding:14px 14px 12px; }
          .cw-feature b{ display:block; margin-bottom:6px; }
          .cw-cta{ margin-top:10px; display:grid; grid-template-columns: 1.2fr .85fr; gap:14px; align-items:center; }
          @media (max-width: 520px){ .cw-cta{ grid-template-columns: 1fr; } }
          .cw-note{ color: var(--ink-muted); font-size:.92rem; margin-top:8px; }
          .cw-hero{
            position:relative; height: 560px;
          }
          @media (max-width: 1100px){
            .cw-hero{ height: 340px; margin-top: 8px; }
          }
          .cw-hero img{
            position:absolute; inset:auto; max-width:100%; width: 840px;
            filter: drop-shadow(0 30px 50px rgba(2,6,23,.22));
          }
          .cw-hero.right img{ right:-60px; }
          .cw-hero.left img{ left:-60px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # choose image and alignment
    img_src = IMAGE_FOR[key]
    align_class = "right" if key == "loved" else "left"  # match comps: loved collage on right

    # Defensive: surface a one-line debug if path is missing
    if not _exists(img_src):
        st.caption(f"DEBUG: missing collage at {img_src}. Put your PNG in static/images.")

    # content row
    st.markdown('<div class="cw-wrap"><div class="cw-row">', unsafe_allow_html=True)

    # --- card column
    st.markdown('<div class="cw-card" style="position:relative;">', unsafe_allow_html=True)
    st.markdown('<div class="cw-close">x</div>', unsafe_allow_html=True)

    left, right = PILL[key]
    # visual pills; wrappers control which page we are on
    pill_html = f"""
      <div class="cw-pillbar">
        <span class="cw-pill {'active' if key == 'loved' else ''}">{left}</span>
        <span class="cw-pill {'active' if key == 'you' else ''}">{right}</span>
      </div>
    """
    st.markdown(pill_html, unsafe_allow_html=True)

    st.markdown(f'<div class="cw-head">{HEADLINE[key]}</div>', unsafe_allow_html=True)

    # three tiny features (from original contextual copy)
    features = [
        ("Personalized guidance",
         "Answer a few context questions and we will highlight the first moves to make."),
        ("Care Planning Hub",
         "Navigate between the Guided Care Plan, Cost Planner, and advisor handoff easily."),
        ("Ready for handoff",
         "We will focus on what matters most for you - clarity, confidence, and next steps."),
    ]
    st.markdown('<div class="cw-grid3">', unsafe_allow_html=True)
    for title, desc in features:
        st.markdown(f'<div class="cw-feature"><b>{title}</b><span>{desc}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # name input + CTA
    col_name, col_btn = st.columns([1.2, 0.85])
    with col_name:
        name = st.text_input(NAME_LABEL[key], key=f"cw_name_{key}")
    with col_btn:
        if st.button("Continue", type="primary", use_container_width=True, key=f"cw_continue_{key}"):
            # stash name into a friendly context bucket
            ctx = st.session_state.setdefault(
                "care_context",
                {"person_name": "Your Loved One", "gcp_answers": {}, "gcp_recommendation": None},
            )
            if key == "you":
                ctx["person_name"] = name or "You"
            else:
                ctx["person_name"] = name or "Your Loved One"
            safe_switch_page("pages/hub.py")

    st.markdown(f'<div class="cw-note">{FOOTNOTE}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end card

    # --- collage column
    st.markdown(f'<div class="cw-hero {align_class}">', unsafe_allow_html=True)
    st.markdown(f'<img alt="collage" src="/{img_src}">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
