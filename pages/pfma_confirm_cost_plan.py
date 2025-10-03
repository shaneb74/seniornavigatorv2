
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Cost Plan Confirmer")
st.caption("Confirm your cost plan summary. If something looks off, go back to edit, then return here.")

st.markdown('---')
st.subheader("Summary")

estimate = ctx.get('cost_estimate', {}) if isinstance(ctx.get('cost_estimate', {}), dict) else {}
setting = estimate.get('setting_label') or estimate.get('setting') or "In-home care"
monthly = estimate.get('estimate_monthly')
zip_code = estimate.get('zip')

line = f"{setting}"
if isinstance(monthly, (int, float)) and monthly > 0:
    line += f" * ${monthly:,.0f}/mo"
if zip_code:
    line += f" * ZIP {zip_code}"

st.write(line or "Quick estimate details will appear here.")

st.markdown('---')
agreed = st.checkbox("This looks right", key="pfma_confirm_cost_plan_agree", value=False)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Back to Cost Planner", key="pfma_cost_back"):
        st.switch_page("pages/cost_planner_modules.py")
with col2:
    if st.button("Back to PFMA", key="pfma_cost_pfma"):
        st.switch_page("pages/pfma.py")
with col3:
    if st.button("Next", key="pfma_cost_next", disabled=not agreed):
        st.switch_page("pages/pfma_confirm_care_needs.py")

st.markdown('</div>', unsafe_allow_html=True)