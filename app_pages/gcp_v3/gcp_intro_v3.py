from ui.theme import inject_theme
inject_theme()

import streamlit as st

# Wrapper
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.title("Find the Right Senior Care")

st.write(
    "We know choosing care can feel overwhelming. This quick Guided Care Plan will gather a few details "
    "and suggest options that balance independence, safety, and budget. You can adjust or skip sections anytime."
)

# Simple call-to-action card
with st.container():
    st.markdown('<div class="sn-card" style="padding:1rem;border-radius:1rem;">', unsafe_allow_html=True)
    st.subheader("Ready to begin?")
    st.write("It takes just a few minutes.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Started", type="primary", use_container_width=True):
            try:
                st.switch_page("app_pages/gcp_v3/gcp_eligibility_v3.py")
            except Exception:
                st.session_state["_target_page"] = "app_pages/gcp_v3/gcp_eligibility_v3.py"
                st.rerun()
    with col2:
        if st.button("Back to Care Hub", use_container_width=True):
            try:
                st.switch_page("app_pages/hub.py")
            except Exception:
                st.session_state["_target_page"] = "app_pages/hub.py"
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Close wrapper
st.markdown("</div>", unsafe_allow_html=True)