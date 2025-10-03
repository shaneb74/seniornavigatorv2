import streamlit as st
st.title("Sign in")
st.caption("Prototype login — sets a session flag only.")
c1,c2,c3=st.columns(3)
with c1:
    if st.button("  Sign in with Apple"):
        st.session_state.is_authenticated=True; st.switch_page("pages/hub.py")
with c2:
    if st.button("G  Sign in with Google"):
        st.session_state.is_authenticated=True; st.switch_page("pages/hub.py")
with c3:
    if st.button("f  Sign in with Facebook"):
        st.session_state.is_authenticated=True; st.switch_page("pages/hub.py")
st.markdown("---")
if st.button("Continue with Email"):
    st.session_state.is_authenticated=True; st.switch_page("pages/hub.py")
