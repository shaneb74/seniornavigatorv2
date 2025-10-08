from ui.theme import inject_theme
inject_theme()

import streamlit as st

# ---------- Wrapper ----------
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.title("Daily Life & Support")

# Session defaults
st.session_state.setdefault("gcp_v3.answers", {})
ans = st.session_state["gcp_v3.answers"]

# Overall help (Q3)
overall_help = st.selectbox(
    "Overall, how much help is needed with day-to-day life?",
    ["Select one…", "None", "Occasional", "Regular", "Extensive"],
    index=["Select one…", "None", "Occasional", "Regular", "Extensive"].index(ans.get("overall_help", "Select one…")),
    help="Choose the best match for the level of help needed.",
    key="gcp_v3_overall_help",
)
ans["overall_help"] = overall_help

skip_adls = overall_help == "None"

if not skip_adls:
    st.subheader("Basic Activities of Daily Living (BADLs)")
    badls = st.multiselect(
        "Areas where help is needed (choose all that apply):",
        ["Bathing", "Dressing", "Toileting", "Transferring", "Continence", "Eating"],
        default=ans.get("badls", []),
        key="gcp_v3_badls",
    )
    ans["badls"] = badls

    st.subheader("Instrumental Activities of Daily Living (IADLs)")
    iadls = st.multiselect(
        "Areas where help is needed (choose all that apply):",
        ["Meal Prep", "Housekeeping", "Laundry", "Shopping", "Transportation", "Finances", "Med Management", "Phone/Tech"],
        default=ans.get("iadls", []),
        key="gcp_v3_iadls",
    )
    ans["iadls"] = iadls
else:
    ans["badls"] = []
    ans["iadls"] = []

st.subheader("Support Pattern")
colA, colB = st.columns(2)
with colA:
    hours = st.number_input(
        "Approx. hours of help per day",
        min_value=0.0, step=0.5, value=float(ans.get("hours_per_day", 0.0)),
        key="gcp_v3_hours_per_day",
    )
    ans["hours_per_day"] = hours

with colB:
    who = st.text_input(
        "Who primarily provides support?",
        value=ans.get("who_supports", ""),
        key="gcp_v3_who_supports",
    )
    ans["who_supports"] = who

st.divider()

# ---------- Nav ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("Back"):
        try:
            st.switch_page("app_pages/gcp_v3/gcp_eligibility_v3.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_eligibility_v3.py"
            st.rerun()

with col2:
    if st.button("Next", type="primary"):
        try:
            st.switch_page("app_pages/gcp_v3/gcp_health_safety_v3.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_health_safety_v3.py"
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)