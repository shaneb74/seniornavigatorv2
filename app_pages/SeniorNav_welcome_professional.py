from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import streamlit as st

from app_pages.seniornav_util import ensure_aud, top_nav

PRO_ROLE_OPTIONS = [
    "Discharge Planner",
    "Social Worker",
    "Referral Partner (community/senior living/other)",
    "Case Manager",
    "Other",
]


def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.rerun()


def _image_payload(path: str) -> tuple[str, str] | None:
    file_path = Path(path)
    if not file_path.exists():
        return None
    mime = mimetypes.guess_type(file_path.name)[0] or "image/png"
    data = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return data, mime


def _render_hero_image() -> None:
    for candidate in (
        "static/images/Professional.png",
        "static/images/professional.png",
        "static/images/professional.jpeg",
        "static/images/contextual_welcome_professional.png",
    ):
        payload = _image_payload(candidate)
        if payload:
            data, mime = payload
            st.markdown(
                f"""
                <div style="background: radial-gradient(120% 120% at 80% 10%, #eef2ff 0%, #ffffff 60%);
                            padding: 18px; border-radius: 18px;">
                  <img src="data:{mime};base64,{data}" class="hero-photo"
                       style="width:min(420px, 100%);" alt="Professional advisor reviewing care options with a family">
                </div>
                """,
                unsafe_allow_html=True,
            )
            return
    st.info("Add image at static/images/Professional.png")


def _role_selector(aud: dict) -> bool:
    """Render role selector, return True if a role is selected."""
    selected_role = aud.get("pro_role")
    segmented_available = hasattr(st, "segmented_control")

    if segmented_available:
        choice = st.segmented_control(  # type: ignore[attr-defined]
            "Which best describes your role?",
            options=PRO_ROLE_OPTIONS,
            default=selected_role if selected_role in PRO_ROLE_OPTIONS else None,
            key="sn_pro_role_segment",
        )
    else:
        choice = st.radio(
            "Which best describes your role?",
            options=PRO_ROLE_OPTIONS,
            index=PRO_ROLE_OPTIONS.index(selected_role)
            if selected_role in PRO_ROLE_OPTIONS
            else 0,
        )

    if choice:
        aud["pro_role"] = choice
    return aud.get("pro_role") in PRO_ROLE_OPTIONS


top_nav()

aud = ensure_aud()
aud.setdefault("pro_role", None)
aud["entry"] = "pro"

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

left, right = st.columns([7, 5], gap="large")

with left:
    st.markdown(
        """
        <div style="font-size:clamp(28px,4.2vw,44px);line-height:1.06;font-weight:800;letter-spacing:.2px;margin:0 0 .3rem 0;">
          Concierge Care for Professionals
        </div>
        <div style="font-size:clamp(16px,1.8vw,18px);color:rgba(17,24,39,0.82);font-weight:500;margin:.45rem 0 1rem 0;">
          Fast, no-cost placement support, coordinated by Expert Advisors.
        </div>
        """,
        unsafe_allow_html=True,
    )

    has_role = _role_selector(aud)

    action_cols = st.columns([1, 1], gap="large")
    with action_cols[0]:
        if st.button("Continue", type="primary", use_container_width=True, disabled=not has_role):
            _safe_switch_page("app_pages/SeniorNav_professional_hub.py")
    with action_cols[1]:
        if st.button("Back to Home", type="secondary", use_container_width=True):
            _safe_switch_page("app_pages/welcome.py")

with right:
    _render_hero_image()

st.markdown("</div>", unsafe_allow_html=True)
