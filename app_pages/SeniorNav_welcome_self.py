from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import streamlit as st

from app_pages.seniornav_util import ensure_aud, top_nav


def _safe_switch_page(
    target: str,
    query_key: str | None = None,
    query_value: str | None = None,
) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        if query_key and query_value:
            st.query_params[query_key] = query_value
        st.rerun()


def _goto(path: str, *, query_key: str | None = None, query_value: str | None = None) -> None:
    mapping = {
        "pages/hub.py": "app_pages/hub.py",
        "pages/welcome.py": "app_pages/welcome.py",
        "pages/SeniorNav_login.py": "app_pages/SeniorNav_login.py",
    }
    destination = mapping.get(path, path)
    _safe_switch_page(destination, query_key, query_value)


def _render_hero(image_path: str, alt: str) -> None:
    img_file = Path(image_path)
    if not img_file.exists():
        st.info(f"Add image at {image_path}")
        return
    try:
        mime = mimetypes.guess_type(img_file.name)[0] or "image/png"
        data = base64.b64encode(img_file.read_bytes()).decode("ascii")
        st.markdown(
            f"""
            <div style="background: radial-gradient(120% 120% at 80% 10%, #eef2ff 0%, #ffffff 60%);
                        padding: 18px; border-radius: 18px;">
              <img src="data:{mime};base64,{data}" class="hero-photo"
                   style="width:min(420px, 100%);" alt="{alt}">
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        st.image(str(img_file), use_container_width=True, caption=None)


top_nav()

aud = ensure_aud()
care_context = st.session_state.setdefault("care_context", {"person_name": "You"})

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

left, right = st.columns([7, 5], gap="large")

with left:
    st.markdown("## Planning for yourself?")
    st.write("Share your preferred name so we can personalize the experience for you.")

    name_default = (aud.get("recipient_name") or "").strip()
    entered_name = st.text_input(
        "Preferred name (optional)",
        value=name_default,
        placeholder="e.g., Alex",
    )
    st.caption("You can update this later in the Care Hub.")

    col_continue, _ = st.columns([1, 1])
    with col_continue:
        if st.button("Continue", type="primary", use_container_width=True):
            trimmed = entered_name.strip()
            aud["recipient_name"] = trimmed or None
            aud["entry"] = "self"
            care_context["person_name"] = trimmed or "You"
            _goto("app_pages/hub.py")

    link_cols = st.columns([1, 1])
    with link_cols[0]:
        if st.button("Back to Welcome", type="secondary", use_container_width=True):
            _goto("app_pages/welcome.py")
    with link_cols[1]:
        if st.button("Log in", type="secondary", use_container_width=True):
            _goto("app_pages/SeniorNav_login.py", query_key="view", query_value="login")

with right:
    _render_hero(
        "static/images/Self.png",
        alt="Smiling older adult — planning for myself",
    )

st.markdown("</div>", unsafe_allow_html=True)
