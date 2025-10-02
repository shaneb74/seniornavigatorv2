import streamlit as st
from pathlib import Path

# ---------- Safe navigation helper ----------
def safe_switch(target: str, fallback: str = "pages/hub.py"):
    """Navigate if the target page exists and is registered, otherwise fall back."""
    try:
        if Path(target).exists():
            st.switch_page(target)
        else:
            st.switch_page(fallback)
    except Exception:
        st.switch_page(fallback)

# ---------- UI ----------
st.title("Welcome to the CCA Senior Navigator")
st.caption("Let’s get started by telling us who you’re planning for.")

choice = st.radio(
    "Who are you planning for?",
    ["Myself", "Someone Else", "As a Professional"],
    label_visibility="collapsed",
    key="welcome_choice"
)

st.markdown("---")

if st.button("Continue", key="welcome_continue", use_container_width=True):
    if choice == "Myself":
        safe_switch("pages/tell_us_about_you.py")
    elif choice == "Someone Else":
        safe_switch("pages/tell_us_about_loved_one.py")
    else:
        safe_switch("pages/professional_mode.py")

st.markdown("---")
st.caption("Already have a plan? Jump back to your Hub anytime.")
if st.button("Go to Hub", key="welcome_hub", use_container_width=True):
    safe_switch("pages/hub.py")
