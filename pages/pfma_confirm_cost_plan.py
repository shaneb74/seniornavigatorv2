"""PFMA Cost Planner confirmer."""
from __future__ import annotations

import streamlit as st

st.set_page_config(layout="wide")
from ui.theme import inject_theme
inject_theme()

from ui.pfma import (
    apply_pfma_theme,
    ensure_pfma_state,
    go_to_step,
    render_drawer,
    segmented_control,
    update_section,
)

SECTION_KEY = "cost_plan"
HEALTH_CONDITIONS = (
    "Dementia",
    "Diabetes",
    "Heart condition",
    "Stroke",
    "Parkinson's",
    "Recent surgery",
    "Chronic pain",
)
MOBILITY_OPTIONS = ("Independent", "Uses a cane", "Uses a walker", "Wheelchair", "Bed-bound")

apply_pfma_theme()
state = ensure_pfma_state()
error_placeholder = st.empty()

def _drawer_body(pfma_state: dict[str, object]) -> dict[str, object]:
    section_data = pfma_state["sections"].get(SECTION_KEY, {}).get("data", {})
    cost_state = st.session_state.get("cost_planner", {}) or {}
    audiencing_state = st.session_state.get("audiencing", {}) or {}
    qualifiers = audiencing_state.get("qualifiers", {}) or {}

    st.markdown(
        "<div class='pfma-note'>We pulled cost insights from your recent Cost Planner run. Update anything that changed.</div>",
        unsafe_allow_html=True,
    )

    current_conditions = section_data.get("health_conditions") or cost_state.get("health_conditions") or []
    if isinstance(current_conditions, str):
        current_conditions = [current_conditions]

    st.multiselect(
        "Health considerations we should flag",
        HEALTH_CONDITIONS,
        current_conditions,
        key="pfma_cost_conditions",
        help="Add anything else in the notes box-your advisor will read the full context.",
    )

    mobility_default = section_data.get("mobility") or qualifiers.get("mobility_status")
    segmented_control(
        "Current mobility support",
        MOBILITY_OPTIONS,
        key=f"{SECTION_KEY}_mobility",
        default=mobility_default,
    )

    why_key = f"pfma_{SECTION_KEY}_why_now"
    if why_key not in st.session_state:
        st.session_state[why_key] = section_data.get("why_now") or cost_state.get("notes") or ""
    st.text_area(
        "Why are you planning now?",
        key=why_key,
        max_chars=400,
        height=110,
    )

    monthly_total = cost_state.get("monthly_total")
    offsets = cost_state.get("subtotals", {}).get("offsets") if isinstance(cost_state.get("subtotals"), dict) else None

    return {
        "health_conditions": st.session_state.get("pfma_cost_conditions", []),
        "mobility": st.session_state.get(f"pfma_segment_{SECTION_KEY}_mobility"),
        "why_now": st.session_state[why_key],
        "monthly_total": monthly_total,
        "offsets": offsets,
    }

result = render_drawer(
    step_key=SECTION_KEY,
    title="Cost Planner Confirmer 💡",
    badge="Locks in the Money duck",
    description="Highlight budget factors so the advisor knows how flexible the plan can be.",
    body=_drawer_body,
    footer_note="Need deeper edits? Reopen Cost Planner to refresh the numbers.",
)

if result.saved:
    payload = result.payload
    errors: list[str] = []
    if not payload.get("mobility"):
        errors.append("Tell us the current mobility support so we can prep resources.")
    if errors:
        error_placeholder.error("\n".join(errors))
    else:
        update_section(SECTION_KEY, payload)
        st.toast("Cost context saved for your advisor.")
        if result.next_step:
            go_to_step(result.next_step)
