from __future__ import annotations

import streamlit as st

from app_pages.seniornav_util import ensure_aud, top_nav
from ui.components import ModuleCard, ModuleGrid

PRO_ROLE_OPTIONS = [
    "Discharge Planner",
    "Social Worker",
    "Referral Partner (community/senior living/other)",
    "Case Manager",
    "Other",
]


def _role_selector(aud: dict) -> None:
    segmented_available = hasattr(st, "segmented_control")
    current = aud.get("pro_role")

    if segmented_available:
        choice = st.segmented_control(  # type: ignore[attr-defined]
            "Your role",
            options=PRO_ROLE_OPTIONS,
            default=current if current in PRO_ROLE_OPTIONS else None,
            key="sn_pro_role_segment_hub",
        )
    else:
        choice = st.radio(
            "Your role",
            options=PRO_ROLE_OPTIONS,
            index=PRO_ROLE_OPTIONS.index(current) if current in PRO_ROLE_OPTIONS else 0,
            key="sn_pro_role_radio_hub",
        )

    if choice:
        aud["pro_role"] = choice


top_nav()

aud = ensure_aud()
aud.setdefault("pro_role", None)
aud["entry"] = "pro"

role_label = aud.get("pro_role") or "Professional Partner"

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.markdown("## Professional Mode")
st.caption(f"Welcome, {role_label}")

with st.expander("Update your role", expanded=False):
    _role_selector(aud)

st.markdown("### Tools & Resources")

with ModuleGrid(cols=3, gap="large") as cols:
    with cols[0]:
        ModuleCard(
            icon="💊",
            title="Medication Management",
            body="Quick access to medication review templates, reconciliation checklists, and coordination notes.",
            primary_label="Open Medication Tools",
            on_primary=lambda: None,
            status="not_started",
            testid="pro-card-medication",
        )
    with cols[1]:
        ModuleCard(
            icon="🛡️",
            title="Readmission Risk",
            body="Assess fall risk, hospitalization triggers, and monitoring tasks to stay ahead of readmission.",
            primary_label="Open Readmission Toolkit",
            on_primary=lambda: None,
            status="not_started",
            testid="pro-card-readmission",
        )
    with cols[2]:
        ModuleCard(
            icon="📁",
            title="Professional Planning Resources",
            body="Download referral packets, printable checklists, and community summaries tailored to your clients.",
            primary_label="View Resources",
            on_primary=lambda: None,
            status="not_started",
            testid="pro-card-resources",
        )

st.markdown("</div>", unsafe_allow_html=True)
