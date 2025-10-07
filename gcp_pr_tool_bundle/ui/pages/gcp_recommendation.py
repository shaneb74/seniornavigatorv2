import streamlit as st
from guided_care_plan.engine import evaluate_guided_care
from guided_care_plan.state import get_answers, get_aud

def page():
    st.title("Recommendation")
    answers, aud = get_answers(), get_aud()
    ctx, gcp = evaluate_guided_care(answers, aud)
    st.session_state["gcp_context"] = ctx
    st.session_state["gcp"] = gcp
    # persist unsure for CP
    st.session_state.setdefault("flags", {})["medicaid_unsure"] = bool(ctx.get("medicaid_unsure_flag"))

    if gcp.get("payment_context") == "medicaid" or ctx.get("route") == "medicaid_offramp":
        st.info("**Medicaid/state assistance changes how care is paid.** We'll take you straight to next steps.")
        st.page_link("ui/pages/05_plan_for_my_advisor.py", label="Continue to Plan for My Advisor →")
        st.page_link("ui/pages/03_cost_planner.py", label="Open Cost Planner (optional) →")
    else:
        st.page_link("ui/pages/03_cost_planner.py", label="Open Cost Planner →")

    st.subheader(f"Suggested care type: **{gcp['recommended_setting']}**")
    with st.expander("Why this?"):
        st.json(gcp["DecisionTrace"])
    with st.expander("Debug (context)"):
        st.json(ctx)

    st.page_link("ui/pages/gcp_context_prefs.py", label="← Edit answers")

if __name__ == "__main__":
    page()
