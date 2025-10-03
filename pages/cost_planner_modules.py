import streamlit as st
from ui.theme import inject_theme

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

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

# Quick Estimate tile
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
            st.info("Not started", icon="ℹ️")  # fixed icon

st.markdown('---')

# Other module tiles (simple stubs)
def module_tile(title, caption, key, page):
    with st.container(border=True):
        cols = st.columns([4,2,2])
        with cols[0]:
            st.subheader(title)
            st.caption(caption)
        with cols[1]:
            if st.button("Open", key=key):
                st.switch_page(page)
        with cols[2]:
            st.caption(" ")

module_tile("Home Care Support", "Hourly in‑home caregiving and companion support.", "open_home_care", "pages/cost_planner_home_care.py")
module_tile("Daily Living Aids", "Equipment and supplies that support daily safety and independence.", "open_daily_aids", "pages/cost_planner_daily_aids.py")
module_tile("Housing Path", "Assisted living, memory care, or other residential options.", "open_housing", "pages/cost_planner_housing.py")
module_tile("Benefits Check", "VA, Medicaid, LTC insurance, and other offsets.", "open_benefits", "pages/cost_planner_benefits.py")
module_tile("Age-in-Place Upgrades", "Home safety modifications and accessibility improvements.", "open_mods", "pages/cost_planner_mods.py")

st.markdown('---')
c1, c2 = st.columns(2)
with c1:
    if st.button("Back to Mode", key="mods_back_mode"):
        st.switch_page("pages/cost_planner.py")
with c2:
    if st.button("Expert Review", key="mods_expert_review"):
        st.switch_page("pages/expert_review.py")

st.markdown('</div>', unsafe_allow_html=True)
