import streamlit as st
from pathlib import Path
import base64

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# ---- Inline the hero to avoid any static-path issues on Streamlit Cloud ----
def inline_img(rel_path: str) -> str:
    p = Path(rel_path)
    if not p.exists():
        return ""
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    ext = p.suffix.lower().lstrip(".") or "png"
    return f"data:image/{ext};base64,{b64}"

hero_src = inline_img("static/images/Hero.png")
if hero_src:
    st.markdown(f'''
    <div class="hero-wrap">
      <img class="hero-img" src="{hero_src}" alt="Care hero">
    </div>
    ''', unsafe_allow_html=True)
else:
    st.warning("Hero image not found at `static/images/Hero.png`.")

st.divider()

choice = st.radio("Who are we planning for?", ["Myself", "Someone Else", "I'm a professional"], index=0, key="welcome_choice")
if st.button("Continue", type="primary"):
    if choice == "Myself":
        st.switch_page("pages/tell_us_about_you.py")
    elif choice == "Someone Else":
        st.switch_page("pages/tell_us_about_loved_one.py")
    else:
        st.switch_page("pages/professional_mode.py")