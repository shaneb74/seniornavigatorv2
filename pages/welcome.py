
import streamlit as st

st.title("Entry – Who Are We Planning For?")

# Use segmented control instead of radio, keep label hidden for a11y warning
choice = st.segmented_control(
    "Select who you are planning for",
    options=["Myself", "Someone Else", "I'm a professional"],
    selection_mode="single",
    default="Myself",
    label_visibility="collapsed",
    key="welcome_choice_seg",
)

if st.button("Continue", key="welcome_continue"):
    if choice == "Myself":
        st.switch_page("pages/tell_us_about_you.py")
    elif choice == "Someone Else":
        st.switch_page("pages/tell_us_about_loved_one.py")
    else:
        # Professional requires login in your flow; go to professional mode page
        st.switch_page("pages/professional_mode.py")
