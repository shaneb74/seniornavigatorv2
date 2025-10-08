"""PFMA Personal Info confirmer."""
from __future__ import annotations

import streamlit as st
from ui.pfma import (

apply_pfma_theme,
    ensure_pfma_state,
    go_to_step,
    render_drawer,
    update_section,
)

SECTION_KEY = "personal_info"

apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()

def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})
    booking = pfma_state.get("booking", {})

    st.markdown(
        "<div class='pfma-note'>Double-check contact details so reminders go to the right place.</div>",
        unsafe_allow_html=True,
    )

    name_key = "pfma_personal_name"
    if name_key not in st.session_state:
        st.session_state[name_key] = section_data.get("name") or booking.get("name", "")
    st.text_input("Confirmed name", key=name_key, max_chars=100)

    phone_key = "pfma_personal_phone"
    if phone_key not in st.session_state:
        st.session_state[phone_key] = section_data.get("phone") or booking.get("phone", "")
    st.text_input("Confirmed phone", key=phone_key, max_chars=20)

    email_key = "pfma_personal_email"
    if email_key not in st.session_state:
        st.session_state[email_key] = section_data.get("email") or booking.get("email", "")
    st.text_input("Confirmed email", key=email_key, max_chars=120)

    referral_key = "pfma_personal_referral"
    if referral_key not in st.session_state:
        st.session_state[referral_key] = section_data.get("referral") or booking.get("referral_source", "")
    st.text_input("Referral (if applicable)", key=referral_key, max_chars=200)

    confirm_key = "pfma_personal_confirmed"
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = bool(section_data.get("confirmed"))
    st.checkbox("Everything above is accurate", key=confirm_key)

    return {
        "name": st.session_state[name_key].strip(),
        "phone": st.session_state[phone_key].strip(),
        "email": st.session_state[email_key].strip(),
        "referral": st.session_state[referral_key].strip(),
        "confirmed": st.session_state[confirm_key],
    }

result = render_drawer(
    step_key=SECTION_KEY,
    title="Personal Info 🌟",
    badge="Finishes the You duck",
    description="Confirm how we should address you and where to send follow-ups.",
    body=_drawer_body,
    footer_note="Personal info stays private-only your advisor sees it.",
)

if result.saved:
    payload = result.payload
    errors: list[str] = []
    if not payload.get("name"):
        errors.append("Add the name you want your advisor to use.")
    if not payload.get("phone"):
        errors.append("Confirm a phone number.")
    if not payload.get("confirmed"):
        errors.append("Tick the confirmation to continue.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Contact info confirmed-time for the duck parade! 🦆")
        if result.next_step:
            go_to_step(result.next_step)
