"""PFMA Benefits & Coverage confirmer."""
from __future__ import annotations

import streamlit as st

from ui.theme import inject_theme

inject_theme()

from ui.pfma import (

apply_pfma_theme,
    ensure_pfma_state,
    go_to_step,
    render_drawer,
    update_section,
)

SECTION_KEY = "benefits_coverage"

apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()

def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})

    st.markdown(
        "<div class='pfma-note'>Insurance basics ensure your advisor starts with the right funding paths.</div>",
        unsafe_allow_html=True,
    )

    carrier_key = "pfma_benefits_carrier"
    if carrier_key not in st.session_state:
        st.session_state[carrier_key] = section_data.get("insurance_company", "")
    st.text_input("Primary health insurance", key=carrier_key, placeholder="BlueCross BlueShield")

    ltc_key = "pfma_benefits_ltc"
    if ltc_key not in st.session_state:
        st.session_state[ltc_key] = section_data.get("ltc_insurance", "Yes")
    st.selectbox("Long-term care insurance?", ("Yes", "No", "Unsure"), key=ltc_key)

    medicaid_key = "pfma_benefits_medicaid"
    if medicaid_key not in st.session_state:
        st.session_state[medicaid_key] = section_data.get("medicaid_status", "No")
    st.selectbox("Medicaid status", ("Yes", "No", "Applied", "Unsure"), key=medicaid_key)

    va_key = "pfma_benefits_va"
    if va_key not in st.session_state:
        st.session_state[va_key] = section_data.get("va_eligibility", "No")
    st.selectbox("VA eligibility", ("Yes", "No", "Unsure"), key=va_key)

    verify_key = "pfma_benefits_verified"
    if verify_key not in st.session_state:
        st.session_state[verify_key] = bool(section_data.get("verified"))
    st.checkbox("I've verified this information", key=verify_key)

    return {
        "insurance_company": st.session_state[carrier_key],
        "ltc_insurance": st.session_state[ltc_key],
        "medicaid_status": st.session_state[medicaid_key],
        "va_eligibility": st.session_state[va_key],
        "verified": st.session_state[verify_key],
    }

result = render_drawer(
    step_key=SECTION_KEY,
    title="Benefits & Coverage 💰",
    badge="Proud of the Money duck",
    description="Confirm funding levers so your advisor can fast-track offsets and paperwork.",
    body=_drawer_body,
    footer_note="Not sure on coverage? Share what you know-your advisor will help verify.",
)

if result.saved:
    payload = result.payload
    errors: list[str] = []
    if not payload.get("insurance_company"):
        errors.append("Add the primary insurance carrier.")
    if not payload.get("verified"):
        errors.append("Confirm you've verified the coverage details-or tick it once you do.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Coverage snapshot ready for your advisor.")
        if result.next_step:
            go_to_step(result.next_step)
