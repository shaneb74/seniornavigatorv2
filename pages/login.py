
import streamlit as st
from pathlib import Path

# Session guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

# Candidate targets we conceptually support
_CANDIDATES = [
    "pages/pfma.py",
    "pages/hub.py",
    "pages/cost_planner_modules.py",
    "pages/pfma_confirm_care_plan.py",
]

# Build a runtime-validated allowlist: must be in our conceptual list AND exist on disk
ALLOWED_TARGETS = {t for t in _CANDIDATES if Path(t).exists()}

def safe_go(target: str):
    # If target isn't in the validated allowlist, drop to a safe default
    fallback = "pages/hub.py" if Path("pages/hub.py").exists() else None
    if target not in ALLOWED_TARGETS:
        target = fallback
    if target is None:
        st.error("Navigation target is unavailable.")
    else:
        st.switch_page(target)

# Pick return target: context -> pfma if it exists -> hub
preferred = ctx.get("after_login_target")
if preferred not in ALLOWED_TARGETS:
    preferred = "pages/pfma.py" if "pages/pfma.py" in ALLOWED_TARGETS else "pages/hub.py"

st.title("Sign up")
st.caption(
    "There’s never any cost to you. Creating an account unlocks additional support and benefits.\n"
    "- Assess multiple people with our tools\n"
    "- Eligibility to get additional free benefits\n"
    "- Connect with our advisor for a personalized consultation\n"
)

# Toggle between OAuth and Email
choice = st.radio(
    "Choose a sign-in method",
    ["Continue with...", "Use email"],
    horizontal=True,
    label_visibility="collapsed",
    key="login_method",
)

with st.container(border=True):
    if choice == "Continue with...":
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("  Sign in with Apple", key="oauth_apple", use_container_width=True):
                ctx["is_authenticated"] = True
                safe_go(preferred)
        with c2:
            if st.button("G  Sign in with Google", key="oauth_google", use_container_width=True):
                ctx["is_authenticated"] = True
                safe_go(preferred)
        with c3:
            if st.button("f  Continue with Facebook", key="oauth_facebook", use_container_width=True):
                ctx["is_authenticated"] = True
                safe_go(preferred)
        st.caption("Design mock only. No real authentication.")
    else:
        st.subheader("Email")
        email = st.text_input("Email*", placeholder="Provide your email", key="login_email")
        pwd = st.text_input("Password*", placeholder="Provide your password", type="password", key="login_pwd")
        st.caption("Use 8+ chars, a number, uppercase, and a special character.")
        consent = st.checkbox(
            "I consent to the collection of my consumer health data or have authorization to do so.",
            key="login_consent",
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                "Sign up",
                key="email_signup",
                type="primary",
                disabled=not (email and pwd and consent),
                use_container_width=True,
            ):
                ctx["is_authenticated"] = True
                safe_go(preferred)
        with c2:
            if st.button("I have an account", key="email_have_acct", use_container_width=True):
                ctx["is_authenticated"] = True
                safe_go(preferred)

st.markdown("---")
if st.button("Back to Hub", key="login_back_hub"):
    # Even this checks existence; if hub missing, show a soft error.
    if Path("pages/hub.py").exists():
        st.switch_page("pages/hub.py")
    else:
        st.warning("Hub is unavailable in this build.")
