
import streamlit as st
from pathlib import Path

# Prototype auth flag init
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

def safe_nav(target: str, fallback: str = "pages/hub.py"):
    # Existence check first
    if not Path(target).exists():
        target = fallback if Path(fallback).exists() else None
    try:
        if target:
            st.switch_page(target)
        else:
            st.error("Navigation target is unavailable in this build.")
    except Exception:
        # Likely not registered in st.navigation. Try fallback.
        if Path(fallback).exists():
            try:
                st.switch_page(fallback)
                return
            except Exception:
                pass
        st.error("Could not navigate. Use the sidebar to reach the Hub.")

st.title("Who are we planning for?")

choice = st.radio(
    "Select an option",
    ["Myself", "Someone Else", "I'm a professional"],
    horizontal=True,
    label_visibility="collapsed",
    key="welcome_choice",
)

if st.button("Continue", key="welcome_continue", type="primary"):
    if choice == "Myself":
        safe_nav("pages/tell_us_about_you.py")
    elif choice == "Someone Else":
        safe_nav("pages/tell_us_about_loved_one.py")
    else:
        safe_nav("pages/professional_mode.py", fallback="pages/hub.py")
