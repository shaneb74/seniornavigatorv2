from __future__ import annotations
# Shared renderer for the Contextual Welcome ("For me" / "For someone") pages.

from pathlib import Path
import streamlit as st

# -- safe theme fallback so we don't crash if theme import fails
try:
    from ui.theme import inject_theme
except Exception:  # pragma: no cover
    def inject_theme() -> None:
        st.markdown(
            """
            <style>
              :root{
                --brand:#0b5cd8;         /* primary */
                --ink:#0f172a;           /* text */
                --ink-weak:#4b5563;      /* muted */
                --bg:#ffffff;            /* paper */
                --panel:#f1f5ff;         /* light blue panel */
              }
              .block-container{max-width:1160px}
            </style>
            """,
            unsafe_allow_html=True,
        )


# ---------- content & assets ----------
IMAGE_FOR = {
    # we generated single composite images for each mode
    "self":  "static/images/contextual_welcome_self.png",
    "loved": "static/images/contextual_welcome_someone_else.png",
}

COPY = {
    "self": {
        "h1": "We're here to help you find the support you're looking for.",
        "helper": "The Care Planning Hub is your home base for guided plans, cost tools, and advisor handoffs.",
        "accent": "We'll focus on what matters most for you - clarity, confidence, and next steps.",
    },
    "loved": {
        "h1": "We're here to help you find the support your loved ones need.",
        "helper": "If you want to assess several people, don't worry - you can easily move on to the next step!",
        "accent": "We're alongside you with guidance that keeps family conversations warm and grounded.",
    },
}


def _img_tag(src: str, alt: str = "") -> str:
    # If the file is missing locally, show a subtle placeholder so you know.
    if not Path(src).exists():
        return f'<div class="cw-missing">Missing image: {src}</div>'
    return f'<img class="cw-photo" src="{src}" alt="{alt}"/>'


def render(mode: str) -> None:
    """
    mode: "you" | "self" | "loved"
    Wrapper pages call render("you") or render("loved").
    """
    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="centered")

    # normalize mode key
    key = "self" if mode in {"you", "self"} else "loved"
    img_src = IMAGE_FOR[key]
    text = COPY[key]

    # ---------- CSS ----------
    st.markdown(
        """
        <style>
          /* Stage */
          .cw-stage{
            position: relative;
            min-height: 560px;
            background: linear-gradient(180deg, #f4f7ff 0%, #f8faff 100%);
            border-radius: 24px;
            padding: 40px;
            overflow: hidden;
            box-shadow: 0 8px 28px rgba(16,24,40,.06);
          }

          /* Big collage image on the right */
          .cw-photos{
            position: absolute;
            right: 24px;
            bottom: 24px;
            width: min(58%, 780px);
            pointer-events: none;
          }
          .cw-photo{
            width: 100%;
            height: auto;
            display: block;
            filter: drop-shadow(0 18px 28px rgba(16,24,40,.18));
            user-select: none;
          }
          .cw-missing{
            width: 100%;
            height: 360px;
            display: grid; place-items: center;
            color: #B91C1C; background: #FFF1F2; border: 1px dashed #FCA5A5;
            border-radius: 12px; font-size: 14px; font-family: ui-sans-serif, system-ui, -apple-system;
          }

          /* Modal card (left) */
          .cw-modal{
            position: relative;
            z-index: 1;
            width: min(520px, 100%);
            background: #fff;
            border-radius: 16px;
            padding: 22px 22px 18px;
            box-shadow: 0 14px 46px rgba(16,24,40,.12);
          }

          .cw-tabs{display:flex; gap:10px; margin-bottom:14px}
          .cw-tab{
            border: 0; border-radius: 10px; padding: 8px 14px;
            font-weight: 600; font-size: 14px; line-height: 1;
            background: #0f172a; color: #fff;
          }
          .cw-tab.secondary{ background: #eaf2ff; color: #2b5fd9; }

          .cw-h1{font-size: 22px; font-weight: 800; color: var(--ink); margin: 8px 0 2px;}
          .cw-p  {color: var(--ink-weak); margin: 0 0 12px; font-size: 14px;}

          .cw-name-row{display:flex; gap:12px; align-items:center; margin-top: 6px;}
          .cw-input{
            flex: 1 1 auto;
            border-radius: 10px; border: 1px solid #e5e7eb;
            padding: 12px 14px; font-size: 14px;
            background: #fff;
          }
          .cw-cta{
            border: 0; border-radius: 10px;
            padding: 12px 20px;
            background: #4c64f3; color: #fff; font-weight: 700;
            box-shadow: 0 8px 18px rgba(76,100,243,.35);
            cursor: pointer;
          }
          .cw-helper{ color: var(--ink-weak); font-size: 14px; margin-left: 8px;}

          /* Responsive: stack photo below modal on small screens */
          @media (max-width: 980px){
            .cw-stage{ padding: 24px; }
            .cw-photos{ position: static; width: 100%; margin-top: 14px; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- HTML ----------
    st.markdown('<div class="cw-stage">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="cw-modal">
          <div class="cw-tabs">
            <div class="cw-tab{' ' if key=='loved' else ' secondary'}">For someone</div>
            <div class="cw-tab{' secondary' if key=='loved' else ''}">For me</div>
          </div>

          <div class="cw-h1">{text['h1']}</div>

          <div class="cw-name-row">
            <input class="cw-input" placeholder="What's your name?" />
            <button class="cw-cta">Continue</button>
          </div>

          <div class="cw-p" style="margin-top:10px;">{text['accent']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="cw-photos">{_img_tag(img_src, "decorative collage")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # .cw-stage
