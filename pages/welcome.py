import streamlit as st
from pathlib import Path

# Session guard: keep state consistent
if "care_context" not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# ---------- CSS for card-photo styling ----------
st.markdown(
    """
    <style>
    .card-photo img {
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Helper for safe images ----------
def safe_image(path_str, width=None, css_class=None):
    """
    Renders an image safely.
    - If width is an int, uses that pixel width.
    - Otherwise, defaults to container width.
    - Optionally wraps with a CSS class for styling.
    """
    p = Path(path_str)
    if not p.exists():
        st.info(f"Add image at {path_str}")
        return

    if css_class:
        # Wrap in a styled div
        st.markdown(
            f'<div class="{css_class}"><img src="/{p.as_posix()}" style="width:100%;"></div>',
            unsafe_allow_html=True,
        )
    else:
        if isinstance(width, int):
            st.image(str(p), width=width)
        else:
            st.image(str(p), use_container_width=True)

# ---------- Hero row ----------
left, right = st.columns([7, 5], gap="large")

with left:
    st.markdown("### Concierge Care • Senior Navigator")
    st.markdown(
        """
# Your compassionate  
## guide to senior care decisions
Every care decision matters. We’re here to guide you — at no cost — whether planning for yourself or a loved one.
        """
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")

with right:
    safe_image("static/images/Hero.png", width=520)

st.markdown("---")

# ---------- Two tiles: “How we can help you” ----------
st.subheader("How we can help you")

t1, t2 = st.columns(2, gap="large")

with t1:
    with st.container(border=True):
        safe_image("static/images/Someone-Else.png", css_class="card-photo")
        st.markdown("**I would like to support my loved ones**")
        st.caption("For someone")
        if st.button("Continue", key="tile_someone"):
            st.switch_page("pages/tell_us_about_loved_one.py")

with t2:
    with st.container(border=True):
        safe_image("static/images/Myself.png", css_class="card-photo")
        st.markdown("**I’m looking for support just for myself**")
        st.caption("For myself")
        if st.button("Continue", key="tile_myself"):
            st.switch_page("pages/tell_us_about_you.py")

st.markdown("")
c_only = st.container()
with c_only:
    if st.button("For professionals", key="for_pros"):
        st.switch_page("pages/professional_mode.py")
