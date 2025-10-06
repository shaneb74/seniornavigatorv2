from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav, safe_switch

st.set_page_config(layout="wide", page_title="Sign in")
inject_theme()
top_nav()

st.markdown("## Sign in")
st.caption("Use a social account or your email to continue.")

auth = st.session_state.get("is_authenticated", False)
st.session_state.is_authenticated = auth

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("  Sign in with Apple", use_container_width=True):
        st.session_state.is_authenticated = True
        st.success("Signed in.")
        safe_switch("pages/guided_care_hub.py")
with col2:
    if st.button("G  Sign in with Google", use_container_width=True):
        st.session_state.is_authenticated = True
        st.success("Signed in.")
        safe_switch("pages/guided_care_hub.py")
with col3:
    if st.button("f  Continue with Facebook", use_container_width=True):
        st.session_state.is_authenticated = True
        st.success("Signed in.")
        safe_switch("pages/guided_care_hub.py")

st.divider()

mode = st.session_state.get("login_mode", "social")
link_label = "Sign in with email instead" if mode == "social" else "Use social sign in instead"
if st.button(link_label):
    st.session_state.login_mode = "email" if mode == "social" else "social"
    st.rerun()

if st.session_state.get("login_mode", "social") == "email":
    with st.form("email_login", clear_on_submit=False):
        email = st.text_input("Email address", placeholder="you@example.com")
        pw = st.text_input("Password", type="password", placeholder="********")
        consent = st.checkbox("I consent and have proper authorization if signing up for someone else.")
        can_submit = bool(email.strip()) and bool(pw.strip()) and consent
        submitted = st.form_submit_button("Sign in", type="primary", disabled=not can_submit, use_container_width=True)
        if submitted:
            st.session_state.is_authenticated = True
            st.success("Signed in.")
            safe_switch("pages/guided_care_hub.py")

st.caption("By continuing you agree to our Terms & Privacy.")
cols = st.columns(2)
with cols[0]:
    st.page_link("pages/SeniorNav_terms.py", label="Terms of Use", icon="📄")
with cols[1]:
    st.page_link("pages/SeniorNav_privacy.py", label="Privacy Policy", icon="🔒")

# Footer
cols = st.columns(2)
if hasattr(st, "page_link"):
    with cols[0]:
        st.page_link("pages/SeniorNav_terms.py", label="Terms of Use", icon="📑")
    with cols[1]:
        st.page_link("pages/SeniorNav_privacy.py", label="Privacy Policy", icon="🔒")
else:
    with cols[0]:
        if st.button("Terms of Use"):
            safe_switch("pages/SeniorNav_terms.py")
    with cols[1]:
        if st.button("Privacy Policy"):
            safe_switch("pages/SeniorNav_privacy.py")
