import streamlit as st

# ---------- Session guard ----------
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,
        "gcp_cost": None,
    }

ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")

st.title("Your Concierge Care Hub")
st.caption("Everything in one place. Start with the Guided Care Plan, then explore costs, or connect with an advisor.")
st.markdown("---")

# ---------- Guided Care Plan tile ----------
gcp_completed = bool(ctx.get("gcp_recommendation")) or bool(ctx.get("gcp_answers"))
rec_text = ctx.get("gcp_recommendation") or "Recommendation here"
cost_text = ctx.get("gcp_cost") or "Cost TBD"

with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Guided Care Plan")
        st.caption(f"{rec_text} • {cost_text}" if gcp_completed else "Answer 12 simple questions to get a personalized recommendation.")
    with mid:
        if st.button("Start Plan" if not gcp_completed else "Open", key="hub_gcp_start"):
            st.switch_page("pages/gcp.py")
    with right:
        st.success("Completed", icon="✅") if gcp_completed else st.info("Not started", icon="ℹ️")

# ---------- Cost Planner ----------
st.markdown("---")
with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Cost Planner")
        st.caption("Estimate costs quickly, or build a detailed plan with modules.")
    with mid:
        if st.button("Open Planner", key="hub_open_cp"):
            st.switch_page("pages/cost_planner.py")
    with right:
        st.caption(" ")

# ---------- PFMA ----------
with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Plan for My Advisor")
        st.caption("Book time with a concierge advisor and share your plan.")
    with mid:
        if st.button("Get Connected", key="hub_pfma"):
            st.switch_page("pages/pfma.py")
    with right:
        st.caption(" ")

# ---------- Medication Management ----------
with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Medication Management")
        st.caption("Keep meds on track with simple reminders and checks.")
    with mid:
        if st.button("Open", key="hub_meds"):
            st.switch_page("pages/medication_management.py")
    with right:
        st.caption(" ")

# ---------- Risk Navigator ----------
with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Risk Navigator")
        st.caption("Quick safety check to reduce avoidable risks at home.")
    with mid:
        if st.button("Run Check", key="hub_risk"):
            st.switch_page("pages/risk_navigator.py")
    with right:
        st.caption(" ")

# ---------- Assessment ----------
st.markdown("---")
with st.container(border=True):
    left, mid, right = st.columns([6, 2, 2])
    with left:
        st.subheader("Assessment")
        st.caption("Additional screening tools and forms.")
    with mid:
        if st.button("Open Assessment", key="hub_assess"):
            st.switch_page("pages/care_plan_confirm.py")
    with right:
        st.caption(" ")
