from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import ensure_aud, safe_switch, top_nav

st.set_page_config(layout="wide", page_title="Welcome")
inject_theme()
aud = ensure_aud()
top_nav()

IMAGE_MAP = {
    "self": "static/images/contextual_welcome_self.png",
    "proxy": "static/images/contextual_welcome_proxy.png",
    "professional": "static/images/contextual_welcome_professional.png",
}

COPY = {
    "self": {
        "headline": "Let’s get you oriented.",
        "placeholder": "What is your name?",
    },
    "proxy": {
        "headline": "Who are you helping?",
        "placeholder": "What is their name?",
    },
    "professional": {
        "headline": "We’re here to streamline care planning for your clients.",
        "placeholder": "What is your name?",
    },
}

def render(kind: str):
    inject_theme()
    cols = st.columns([1,1])
    with cols[0]:
        st.markdown(f"## {COPY[kind]['headline']}")
    with cols[1]:
        st.image(IMAGE_MAP.get(kind, ""), use_container_width=True, caption="")

    st.markdown('<div class="sn-card">', unsafe_allow_html=True)
    if kind == "self":
        aud["entry"] = "self"
        aud["recipient_name"] = st.text_input("Your name", value=aud.get("recipient_name",""), placeholder=COPY["self"]["placeholder"])
        disabled = not bool(aud["recipient_name"].strip())
        if st.button("Continue", type="primary", use_container_width=True, disabled=disabled):
            if not aud["recipient_name"].strip():
                aud["recipient_name"] = "You"
            safe_switch('pages/guided_care_hub.py')
    elif kind == "proxy":
        aud["entry"] = "proxy"
        aud["recipient_name"] = st.text_input("Their name", value=aud.get("recipient_name",""), placeholder=COPY["proxy"]["placeholder"])
        rel_opts = [
            "Parent","Spouse/Partner","Adult Child","Sibling","Other Relative","Friend/Neighbor","Professional Caregiver","POA / Case Manager","Other","Prefer not to say"
        ]
        rel = st.selectbox("Relationship", rel_opts, index=(rel_opts.index(aud.get("relationship_label")) if aud.get("relationship_label") in rel_opts else 0))
        aud["relationship_label"] = rel
        aud["relationship_code"] = rel.lower().replace(" / ","_").replace(" ","_")
        if rel == "Other":
            aud["relationship_other"] = st.text_input("Describe your relationship (optional)", value=aud.get("relationship_other",""))
        disabled = not bool(aud["recipient_name"].strip()) or not bool(aud["relationship_code"])
        if st.button("Continue", type="primary", use_container_width=True, disabled=disabled):
            if not aud["recipient_name"].strip():
                aud["recipient_name"] = "Your Loved One"
            safe_switch('pages/guided_care_hub.py')
    else:
        aud["entry"] = "professional"
        aud["recipient_name"] = st.text_input("Your name", value=aud.get("recipient_name",""), placeholder=COPY["professional"]["placeholder"])
        ptype = st.selectbox("Your role", ["Case Manager","Discharge Planner"], index=(["Case Manager","Discharge Planner"].index(aud.get("professional_type")) if aud.get("professional_type") in ["Case Manager","Discharge Planner"] else 0))
        aud["professional_type"] = ptype
        disabled = not bool(aud["recipient_name"].strip()) or not bool(aud["professional_type"])
        if st.button("Continue", type="primary", use_container_width=True, disabled=disabled):
            if not aud["recipient_name"].strip():
                aud["recipient_name"] = "Your Client"
            safe_switch("pages/SeniorNav_professional_hub.py")
    st.markdown('</div>', unsafe_allow_html=True)
