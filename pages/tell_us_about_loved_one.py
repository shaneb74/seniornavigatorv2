from ui.ux_enhancements import apply_global_ux, render_stepper
import streamlit as st

apply_global_ux()
render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'professional_role': None,
        'people': [],
        'care_flags': {},
        'derived_flags': {}
    }
ctx = st.session_state.care_context


st.header("Tell Us About Your Loved One")
st.write("A few quick details help us guide you. These toggles set simple yes/no flags for planning logic later.")

col1, col2, col3 = st.columns(3)
with col1:
    is_veteran = st.checkbox("Served in the military?", value=ctx['care_flags'].get('is_veteran', False), key='is_veteran_checkbox')
with col2:
    has_medicaid = st.checkbox("Medicaid today?", value=ctx['care_flags'].get('has_medicaid', False), key='has_medicaid_checkbox')
with col3:
    owns_home = st.checkbox("Own a home?", value=ctx['care_flags'].get('owns_home', False), key='owns_home_checkbox')

# Persist flags
ctx['care_flags']['is_veteran'] = bool(st.session_state.get('is_veteran_checkbox', False))
ctx['care_flags']['has_medicaid'] = bool(st.session_state.get('has_medicaid_checkbox', False))
ctx['care_flags']['owns_home'] = bool(st.session_state.get('owns_home_checkbox', False))

st.caption("These are not disqualifiers. They just help us tailor your path.")

st.markdown('<div class="sn-sticky-bottom">', unsafe_allow_html=True)
c1, c2 = st.columns([1,1])
with c1:
    if st.button("Back: Audiencing"):
        st.switch_page('pages/audiencing.py')
with c2:
    if st.button("Next: Care Needs"):
        st.switch_page('pages/care_needs.py')
st.markdown('</div>', unsafe_allow_html=True)
