import streamlit as st
from pathlib import Path

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "care_context" not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context

ALLOWED_TARGETS = {
    "pages/hub.py",
    "pages/pfma.py",
    "pages/cost_planner.py",
    "pages/cost_planner_modules.py",
    "pages/gcp.py",
    "pages/welcome.py",
}

def page_exists(p: str) -> bool:
    try:
        return Path(p).exists()
    except Exception:
        return False

def safe_go(target: str):
    if target not in ALLOWED_TARGETS or not page_exists(target):
        target = "pages/hub.py"
    st.switch_page(target)

ret = st.session_state.get("after_login_target") or "pages/hub.py"

st.title("Sign in")
st.caption("Prototype sign-in. Choose an option to mark this session as signed in and return to where you were going.")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("  Sign in with Apple", key="oauth_apple", use_container_width=True):
        st.session_state.is_authenticated = True
        ctx["auth_provider"] = "apple"
        safe_go(ret)
with c2:
    if st.button("G  Sign in with Google", key="oauth_google", use_container_width=True):
        st.session_state.is_authenticated = True
        ctx["auth_provider"] = "google"
        safe_go(ret)
with c3:
    if st.button("f  Continue with Facebook", key="oauth_fb", use_container_width=True):
        st.session_state.is_authenticated = True
        ctx["auth_provider"] = "facebook"
        safe_go(ret)

st.markdown("— or —")

email = st.text_input("Email")
pw = st.text_input("Password", type="password")
if st.button("Sign in with email", key="email_login"):
    st.session_state.is_authenticated = True
    ctx["auth_provider"] = "email"
    safe_go(ret)

st.markdown("---")
if st.button("Back to Hub", key="back_hub_login"):
    st.switch_page("pages/hub.py")
