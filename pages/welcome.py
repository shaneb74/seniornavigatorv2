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
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Helper for safe images (NO width=None) ----------
def safe_image(path_str, width="stretch", css_class=None):
    """
    Renders an image safely.

    width:
      - int: pixel width (e.g., 520)
      - 'stretch': expand to container width
      - 'content': natural image width
    """
    p = Path(path_str)
    if not p.exists():
        st.info(f"Add image at {path_str}")
        return

    # If you want CSS styling, use a small HTML wrapper but still let Streamlit handle the image
    # via its served URL. Otherwise just call st.image.
    if isinstance(width, int):
        if css_class:
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            st.image(str(p), width=width)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.image(str(p), width=width)
    else:
        # Accept only the new valid strings; default to 'stretch'
        if width not in ("stretch", "content"):
            width = "stretch"
        if css_class:
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            st.image(str(p), width=width)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.image(str(p), width=width)

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
    # Fixed pixel width for hero
    safe_image("static/images/Hero.png", width=520)

st.markdown("---")

# ---------- Two tiles: “How we can help you” ----------
st.subheader("How we can help you")

t1, t2 = st.columns(2, gap="large")

with t1:
    with st.container(border=True):
        # Stretch to container width with rounded/shadow styling
        safe_image("static/images/Someone-Else.png", width="stretch", css_class="card-photo")
        st.markdown("**I would like to support my loved ones**")
        st.caption("For someone")
        if st.button("Continue", key="tile_someone"):
            st.switch_page("pages/tell_us_about_loved_one.py")

with t2:
    with st.container(border=True):
        # Stretch to container width with rounded/shadow styling
        safe_image("static/images/Myself.png", width="stretch", css_class="card-photo")
        st.markdown("**I’m looking for support just for myself**")
        st.caption("For myself")
        if st.button("Continue", key="tile_myself"):
            st.switch_page("pages/tell_us_about_you.py")

st.markdown("")
c_only = st.container()
with c_only:
    if st.button("For professionals", key="for_pros"):
        st.switch_page("pages/professional_mode.py")
