import streamlit as st

# Guard
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,  # 'None' | 'In-home care' | 'Assisted living' | 'Memory care'
        "gcp_cost": None,            # e.g., "$5,200/mo"
    }

ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")

st.title("Your Concierge Care Hub")
st.caption("Everything in one place. Start with the Guided Care Plan, then explore costs, or connect with an advisor.")
st.markdown("---")

# Guided Care Plan (top)
gcp_done = bool(ctx.get("gcp_recommendation")) or bool(ctx.get("gcp_answers"))
rec_text = ctx.get("gcp_recommendation") or "Recommendation here"
cost_text = ctx.get("gcp_cost") or "Cost TBD"

with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Guided Care Plan")
        if gcp_done:
            st.caption(f"{rec_text} • {cost_text}")
        else:
            st.caption("Answer 12 simple questions to get a personalized recommendation.")
    with mid:
        label = "Start Plan" if not gcp_done else "Open"
        if st.button(label, key="hub_gcp_start"):
            st.switch_page("pages/gcp.py")
    with right:
        if gcp_done:
            st.success("Completed", icon="✅")
        else:
            st.info("Not started")

# Cost Planner
st.markdown("---")
with st.container(border=True):
    left, mid, _ = st.columns([6, 2, 2])
    with left:
        st.subheader("Cost Planner")
        st.caption("Estimate costs quickly, or build a detailed plan with modules.")
    with mid:
        if st.button("Open Planner", key="hub_open_cp"):
            st.switch_page("pages/cost_planner.py")

# Plan for My Advisor
with st.container(border=True):
    left, mid, _ = st.columns([6, 2, 2])
    with left:
        st.subheader("Plan for My Advisor")
        st.caption("Book time with a concierge advisor and share your plan.")
    with mid:
        if st.button("Get Connected", key="hub_pfma"):
            st.switch_page("pages/pfma.py")

# Medication Management
with st.container(border=True):
    left, mid, _ = st.columns([6, 2, 2])
    with left:
        st.subheader("Medication Management")
        st.caption("Keep meds on track with simple reminders and checks.")
    with mid:
        if st.button("Open", key="hub_meds"):
            st.switch_page("pages/medication_management.py")

# Risk Navigator
with st.container(border=True):
    left, mid, _ = st.columns([6, 2, 2])
    with left:
        st.subheader("Risk Navigator")
        st.caption("Quick safety check to reduce avoidable risks at home.")
    with mid:
        if st.button("Run Check", key="hub_risk"):
            st.switch_page("pages/risk_navigator.py")

# Assessment (last)
st.markdown("---")
with st.container(border=True):
    left, mid, _ = st.columns([6, 2, 2])
    with left:
        st.subheader("Assessment")
        st.caption("Additional screening tools and forms.")
    with mid:
        if st.button("Open Assessment", key="hub_assess"):
            st.switch_page("pages/care_plan_confirm.py")
