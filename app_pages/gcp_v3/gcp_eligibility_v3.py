from ui.theme import inject_theme
inject_theme()

import streamlit as st

# ---------- Wrapper ----------
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.title("Eligibility")

st.write(
    "To tailor your experience, please answer a quick eligibility question. "
    "This will not block your ability to use the Cost Planner."
)

# Session defaults
st.session_state.setdefault("medicaid_status", None)

# --- Medicaid question with placeholder option ---
OPTIONS = ["Select one…", "Yes", "No"]

stored = st.session_state.get("medicaid_status")
if stored == "yes":
    idx = 1
elif stored == "no":
    idx = 2
else:
    idx = 0  # placeholder

choice = st.radio(
    "Are you currently on **Medicaid** (state long-term care assistance, not Medicare)?",
    options=OPTIONS,
    index=idx,
    help="This helps us show the right guidance. It does not stop you from using the Cost Planner.",
    key="gcp_v3_medicaid_radio",
)

# Persist back to session + show info
if choice == "Yes":
    st.session_state["medicaid_status"] = "yes"
    st.info(
        "At this time, our placement service can’t assist with Medicaid-based placement. "
        "You can still continue through the app and use the Cost Planner."
    )
elif choice == "No":
    st.session_state["medicaid_status"] = "no"
else:
    st.session_state["medicaid_status"] = None

st.divider()

# ---------- Nav ----------
next_disabled = st.session_state["medicaid_status"] is None
col1, col2 = st.columns(2)
with col1:
    if st.button("Back"):
        try:
            st.switch_page("app_pages/gcp_v3/gcp_intro_v3.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_intro_v3.py"
            st.rerun()

with col2:
    if st.button("Next", type="primary", disabled=next_disabled):
        try:
            st.switch_page("app_pages/gcp_v3/gcp_daily_life_v3.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_daily_life_v3.py"
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)