import streamlit as st

# Cost Plan Confirmation
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Confirm Cost Plan for John")
st.markdown("<h2>Does this fit his budget?</h2>", unsafe_allow_html=True)
st.markdown("<p>Review and lock in the cost summary.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Confirmation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Cost Plan Summary", unsafe_allow_html=True)
st.markdown("<p>Total: $1,500/month (10 hrs home care + aids). Covers John’s needs—adjust if needed later.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="cost_plan_confirm")
st.button("Save Confirmation", key="save_cost_plan", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Care Plan", key="back_cpc", type="secondary")
with col2:
    if st.button("Next: Care Needs", key="next_cpc", type="primary"):
        st.switch_page("pages/care_needs.py")
st.markdown('</div>', unsafe_allow_html=True)
