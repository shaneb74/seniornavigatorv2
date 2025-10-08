from ui.theme import inject_theme
inject_theme()

import streamlit as st

# ---------- Wrapper ----------
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.title("Health & Safety")

# Session defaults
st.session_state.setdefault("gcp_v3.answers", {})
ans = st.session_state["gcp_v3.answers"]
st.session_state.setdefault("gcp_v3.flags", set())
flags = set(st.session_state["gcp_v3.flags"])

# Cognitive
cognitive = st.selectbox(
    "Cognitive status",
    ["Select one…", "Intact", "Mild", "Moderate", "Severe"],
    index=["Select one…", "Intact", "Mild", "Moderate", "Severe"].index(ans.get("cognitive", "Select one…")),
    key="gcp_v3_cognitive",
)
ans["cognitive"] = cognitive

# If cognitive Moderate/Severe -> Behavior risks
behaviors = []
if cognitive in {"Moderate", "Severe"}:
    behaviors = st.multiselect(
        "Behavior risks (choose all that apply):",
        ["Exit seeking", "Wandering", "Agitation", "Aggression", "Sundowning"],
        default=ans.get("behavior_risks", []),
        key="gcp_v3_behavior_risks",
    )
ans["behavior_risks"] = behaviors
flags.discard("behavior_risk")
if behaviors:
    flags.add("behavior_risk")

# Medication profile
med_profile = st.selectbox(
    "Medication profile",
    ["Select one…", "Simple (≤5 meds)", "Moderate (6–9)", "Complex (≥10)"],
    index=["Select one…", "Simple (≤5 meds)", "Moderate (6–9)", "Complex (≥10)"].index(ans.get("med_profile", "Select one…")),
    key="gcp_v3_med_profile",
)
ans["med_profile"] = med_profile

# Mobility & Falls
mobility = st.selectbox(
    "Mobility",
    ["Select one…", "Independent", "Uses device", "Needs assist", "Non-ambulatory"],
    index=["Select one…", "Independent", "Uses device", "Needs assist", "Non-ambulatory"].index(ans.get("mobility", "Select one…")),
    key="gcp_v3_mobility",
)
ans["mobility"] = mobility

falls = st.number_input(
    "Number of falls in last 6 months",
    min_value=0, step=1, value=int(ans.get("falls_6mo", 0)),
    key="gcp_v3_falls_6mo",
)
ans["falls_6mo"] = int(falls)
flags.discard("falls_multiple")
if int(falls) >= 2:
    flags.add("falls_multiple")

# Chronic conditions
chronic = st.multiselect(
    "Chronic conditions (choose all that apply):",
    ["Hypertension", "Diabetes", "CHF", "COPD", "CKD", "Arthritis", "Other"],
    default=ans.get("chronic_conditions", []),
    key="gcp_v3_chronic_conditions",
)
ans["chronic_conditions"] = chronic

mgmt_quality = None
if len(chronic) >= 2:
    mgmt_quality = st.selectbox(
        "How well are chronic conditions managed?",
        ["Select one…", "Well-managed", "Mixed", "Poorly-managed / Unstable"],
        index=["Select one…", "Well-managed", "Mixed", "Poorly-managed / Unstable"].index(ans.get("mgmt_quality", "Select one…")),
        key="gcp_v3_mgmt_quality",
    )
ans["mgmt_quality"] = mgmt_quality

# Mood
mood = st.selectbox(
    "Mood / Outlook",
    ["Select one…", "Stable", "Occasional low mood", "Low"],
    index=["Select one…", "Stable", "Occasional low mood", "Low"].index(ans.get("mood", "Select one…")),
    key="gcp_v3_mood",
)
ans["mood"] = mood

# Geographic isolation
geo = st.selectbox(
    "Geographic isolation",
    ["Select one…", "Not isolated", "Somewhat isolated", "Isolated (rural / limited support)"],
    index=["Select one…", "Not isolated", "Somewhat isolated", "Isolated (rural / limited support)"].index(ans.get("geo_isolation", "Select one…")),
    key="gcp_v3_geo_isolation",
)
ans["geo_isolation"] = geo
flags.discard("geo_isolated")
if geo == "Isolated (rural / limited support)":
    flags.add("geo_isolated")

# Persist flags set
st.session_state["gcp_v3.flags"] = flags

st.divider()

# ---------- Nav ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("Back"):
        try:
            st.switch_page("app_pages/gcp_v3/gcp_daily_life_v3.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_daily_life_v3.py"
            st.rerun()

with col2:
    if st.button("Next", type="primary"):
        try:
            st.switch_page("app_pages/gcp_v3/gcp_results_v3.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_results_v3.py"
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)