import streamlit as st
from pathlib import Path

# Ensure CSS is injected
css_path = Path("static/style.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

hero_path = Path("static/images/Hero.png")
if hero_path.exists():
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    st.image(str(hero_path), use_container_width=False, width=600, caption=None, output_format="PNG")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Hero image not found at static/images/Hero.png")

st.divider()

choice = st.radio("Who are we planning for?", ["Myself","Someone Else","I'm a professional"], index=0, key="welcome_choice")
if st.button("Continue", type="primary"):
    if choice=="Myself":
        st.switch_page("pages/tell_us_about_you.py")
    elif choice=="Someone Else":
        st.switch_page("pages/tell_us_about_loved_one.py")
    else:
        st.switch_page("pages/professional_mode.py")
