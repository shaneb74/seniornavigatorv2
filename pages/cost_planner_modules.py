
import streamlit as st

# Session-state guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'estimating',
        'care_flags': {},
        'person_name': 'Your Loved One',
        'cost_estimate': {}
    }

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')
estimate = ctx.get('cost_estimate', {})
est_completed = bool(estimate.get('completed'))
est_setting = estimate.get('setting_label') or estimate.get('setting') or ''
est_zip = estimate.get('zip', '')
est_monthly = estimate.get('estimate_monthly')

st.title(f"Recommended Cost Modules for {person_name}")
st.caption("Work through the modules below. You can return to any module at any time.")

st.markdown('---')

# ===== New: Cost of Care Planner (Quick Estimate) tile =====
with st.container(border=True):
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.subheader("Cost of Care Planner")
        if est_completed and est_monthly:
            summary = f"{est_setting or 'In-home care'} • ${est_monthly:,}/mo"
            if est_zip:
                summary += f" • ZIP {est_zip}"
            st.caption(summary)
        else:
            st.caption("Get a quick monthly estimate based on setting, ZIP, and a few simple details.")
    with cols[1]:
        if st.button("Open", key="open_quick_estimate"):
            st.switch_page("pages/cost_planner_estimate.py")
    with cols[2]:
        if est_completed:
            st.success("Completed", icon="✅")
        else:
            st.info("Not started", icon="🛈")

st.markdown('---')

# ===== Existing module tiles (kept consistent with prior wiring) =====
# Home Care Support
with st.container(border=True):
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.subheader("Home Care Support")
        st.caption("Hourly in‑home caregiving and companion support.")
    with cols[1]:
        if st.button("Open", key="open_home_care"):
            st.switch_page("pages/cost_planner_home_care.py")
    with cols[2]:
        st.caption(" ")

# Daily Living Aids
with st.container(border=True):
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.subheader("Daily Living Aids")
        st.caption("Equipment and supplies that support daily safety and independence.")
    with cols[1]:
        if st.button("Open", key="open_daily_aids"):
            st.switch_page("pages/cost_planner_daily_aids.py")
    with cols[2]:
        st.caption(" ")

# Housing Path
with st.container(border=True):
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.subheader("Housing Path")
        st.caption("Assisted living, memory care, or other residential options.")
    with cols[1]:
        if st.button("Open", key="open_housing"):
            st.switch_page("pages/cost_planner_housing.py")
    with cols[2]:
        st.caption(" ")

# Benefits Check
with st.container(border=True):
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.subheader("Benefits Check")
        st.caption("VA, Medicaid, LTC insurance, and other offsets.")
    with cols[1]:
        if st.button("Open", key="open_benefits"):
            st.switch_page("pages/cost_planner_benefits.py")
    with cols[2]:
        st.caption(" ")

# Age-in-Place Upgrades
with st.container(border=True):
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.subheader("Age-in-Place Upgrades")
        st.caption("Home safety modifications and accessibility improvements.")
    with cols[1]:
        if st.button("Open", key="open_mods"):
            st.switch_page("pages/cost_planner_mods.py")
    with cols[2]:
        st.caption(" ")

st.markdown('---')

# Footer nav
col1, col2 = st.columns(2)
with col1:
    if st.button("Back to Mode", key="mods_back_mode"):
        st.switch_page("pages/cost_planner.py")
with col2:
    if st.button("Next: Expert Review", key="mods_next_review"):
        st.switch_page("pages/cost_planner_evaluation.py")
