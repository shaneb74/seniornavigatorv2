"""PFMA summary and exports."""
from __future__ import annotations

import streamlit as st

from ui.pfma import (
    DRAWER_KEYS,
    DUCK_BADGES,
    apply_pfma_theme,
    build_export_payloads,
    duck_parade,
    ensure_pfma_state,
    mark_step_complete,
    render_header,
    render_progress,
    set_badges_from_progress,
)


SECTION_LABELS = {
    "care_plan": "Care Plan Confirmer",
    "cost_plan": "Cost Planner Confirmer",
    "care_needs": "Care Needs & Support",
    "care_prefs": "Care Preferences",
    "household_legal": "Household & Legal",
    "benefits_coverage": "Benefits & Coverage",
    "personal_info": "Personal Info",
}


apply_pfma_theme()
state = ensure_pfma_state()

render_header("Step 9 · Summary & exports")
render_progress("summary")

mark_step_complete("summary")
set_badges_from_progress()

sections = state.get("sections", {})
all_ready = all(sections.get(key, {}).get("complete") for key in DRAWER_KEYS)

st.markdown('<div class="pfma-card">', unsafe_allow_html=True)
st.markdown("<h3>Your ducks are lining up!</h3>", unsafe_allow_html=True)
if all_ready:
    st.success("Every badge is unlocked. Your advisor can jump straight into next steps-great work!")
else:
    st.info("You can still polish details later. Anything marked in progress stays editable.")
st.markdown('</div>', unsafe_allow_html=True)

left, right = st.columns((1.25, 0.9), gap="large")

with left:
    st.markdown('<div class="pfma-card">', unsafe_allow_html=True)
    st.markdown("<h3>Advisor-ready snapshot</h3>", unsafe_allow_html=True)
    for key in DRAWER_KEYS:
        label = SECTION_LABELS.get(key, key.replace("_", " ").title())
        complete = sections.get(key, {}).get("complete")
        status = "Ready" if complete else "In progress"
        badge = "✅" if complete else "⏳"
        st.markdown(
            f"<div class='pfma-summary-row'><span>{badge} {label}</span><span class='status'>{status}</span></div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("View My Advisor Plan", type="primary", key="pfma_view_plan"):
        st.toast("Advisor dossier view coming soon.")
    if st.button("Share your ducks 🦆", key="pfma_share_ducks"):
        st.toast("Snapshot link copied for your advisor-friendly brag!")

    st.markdown("<h4>Duck parade progress</h4>", unsafe_allow_html=True)
    st.markdown('<div class="pfma-wheel">', unsafe_allow_html=True)
    for duck in DUCK_BADGES:
        unlocked = state["badges"].get(duck, False)
        status_text = "Unlocked" if unlocked else "Locked"
        accent = "style='color:#0b5cd8;font-weight:700;'" if unlocked else ""
        st.markdown(
            f"<div class='pfma-wheel__duck'><strong {accent}>{duck}</strong><span>{status_text}</span></div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
    duck_parade()

with right:
    pdf_buffer, csv_buffer = build_export_payloads()
    pdf_buffer.seek(0)
    csv_buffer.seek(0)
    st.markdown('<div class="pfma-download-card">', unsafe_allow_html=True)
    st.markdown("<h3>Exports</h3><p style='margin:0;color:var(--ink-muted);'>Share with family or care pros.</p>", unsafe_allow_html=True)
    st.download_button("Download PFMA (PDF)", data=pdf_buffer, file_name="pfma_summary.pdf", mime="application/pdf")
    st.download_button("Download Data (CSV)", data=csv_buffer, file_name="pfma_data.csv", mime="text/csv")
    st.markdown("<div class=\"pfma-note\">We'll call you soon - check your messages for confirmation.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

