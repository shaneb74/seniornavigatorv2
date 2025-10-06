from __future__ import annotations
import streamlit as st
from pathlib import Path

def _show_if_exists(path, **kwargs):
    import streamlit as st
    if not path:
        return False
    q = Path(path)
    # try exact
    if q.exists():
        st.image(str(q), **kwargs)
        return True
    # try png/jpg swap
    alt = None
    suf = q.suffix.lower()
    if suf == ".png":
        alt = q.with_suffix(".jpg")
    elif suf == ".jpg":
        alt = q.with_suffix(".png")
    if alt and alt.exists():
        st.image(str(alt), **kwargs)
        return True
    return False

from ui.theme import inject_theme
from app_pages.seniornav_util import ensure_aud, safe_switch, top_nav

inject_theme()
top_nav()

IMAGE_MAP = {
    "self": "static/images/contextual_welcome_self.png",
    "proxy": "static/images/contextual_welcome_someone_else.png",
    "professional": "static/images/professional.jpeg",
}

COPY = {
    "self": {
        "headline": "Welcome! We're here to guide you on your care journey.",
        "placeholder": "May we have your name?"
    },
    "proxy": {
        "headline": "Helping someone you care about? Let's start together.",
        "placeholder": "What is their name?"
    },
    "professional": {
        "headline": "Supporting your clients with care planning made simple.",
        "placeholder": "May we have your name?"
    },
}

def _existing_image(path: str | None) -> str | None:
    if not path:
        return None
    p = Path(path)
    if p.exists():
        return str(p)
    if p.suffix.lower() == ".png" and p.with_suffix(".jpg").exists():
        return str(p.with_suffix(".jpg"))
    if p.suffix.lower() == ".jpg" and p.with_suffix(".png").exists():
        return str(p.with_suffix(".png"))
    return None

def render(kind: str):
    inject_theme()
    aud = ensure_aud()
    left, right = st.columns([1, 1])
    with left:
        st.markdown(f"## {COPY[kind]['headline']}")
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)
        if kind == "self":
            aud["entry"] = "self"
            aud["recipient_name"] = st.text_input(
                "Your name",
                value=aud.get("recipient_name", ""),
                placeholder=COPY["self"]["placeholder"],
            )
        elif kind == "proxy":
            aud["entry"] = "proxy"
            aud["recipient_name"] = st.text_input(
                "Their name",
                value=aud.get("recipient_name", ""),
                placeholder=COPY["proxy"]["placeholder"],
            )
            rel_opts = [
                "Parent", "Spouse/Partner", "Adult Child", "Sibling", "Other Relative",
                "Friend/Neighbor", "Professional Caregiver", "POA / Case Manager", "Other", "Prefer not to say",
            ]
            rel = st.selectbox(
                "Your relationship to them",
                rel_opts,
                index=(rel_opts.index(aud.get("relationship_label")) if aud.get("relationship_label") in rel_opts else 0),
            )
            aud["relationship_label"] = rel
            aud["relationship_code"] = ("poa_case_manager" if rel == "POA / Case Manager"
                                      else rel.lower().replace(" / ", "_").replace(" ", "_"))
            if rel == "Other":
                aud["relationship_other"] = st.text_input(
                    "Please describe your relationship (optional)",
                    value=aud.get("relationship_other", ""),
                )
        else:
            aud["entry"] = "professional"
            aud["recipient_name"] = st.text_input(
                "Your name",
                value=aud.get("recipient_name", ""),
                placeholder=COPY["professional"]["placeholder"],
            )
            roles = ["Case Manager", "Discharge Planner"]
            ptype = st.selectbox(
                "Your professional role",
                roles,
                index=(roles.index(aud.get("professional_type")) if aud.get("professional_type") in roles else 0),
            )
            aud["professional_type"] = ptype
        name = (aud.get("recipient_name") or "").strip()
        rel_code = (aud.get("relationship_code") or "").strip()
        pro_type = (aud.get("professional_type") or "").strip()
        if kind == "self":
            disabled = not bool(name)
        elif kind == "proxy":
            disabled = not (name and rel_code)
        else:
            disabled = not (name and pro_type)
        if kind == "self":
            if st.button("Let's Get Started", type="primary", use_container_width=True, disabled=disabled):
                if not name:
                    aud["recipient_name"] = "You"
                safe_switch("pages/guided_care_hub.py")
        elif kind == "proxy":
            if st.button("Let's Get Started", type="primary", use_container_width=True, disabled=disabled):
                if not name:
                    aud["recipient_name"] = "Your Loved One"
                safe_switch("pages/guided_care_hub.py")
        else:
            if st.button("Let's Get Started", type="primary", use_container_width=True, disabled=disabled):
                if not name:
                    aud["recipient_name"] = "Your Client"
                safe_switch("pages/SeniorNav_professional_hub.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        img = _existing_image(IMAGE_MAP.get(kind))
        if img:
            _show_if_exists(img, use_container_width=True)
