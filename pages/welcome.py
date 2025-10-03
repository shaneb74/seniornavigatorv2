import io
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

# ------------------ Settings ------------------
st.set_page_config(layout="wide")

# Keep state
if "care_context" not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# ------------------ CSS ------------------
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.25rem; padding-bottom: 3rem; }

      /* HERO */
      .hero-wrap { display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 3rem; align-items: center; }
      @media (max-width: 1100px) { .hero-wrap { grid-template-columns: 1fr; gap: 1.25rem; } }

      .hero-h1 {
        font-size: clamp(26px, 3.6vw, 40px);  /* toned down */
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: .2px;
        margin: 0 0 .25rem 0;
      }
      .hero-h2 {
        font-size: clamp(16px, 1.7vw, 18px);
        color: rgba(0,0,0,0.72);
        font-weight: 500;
        margin: .5rem 0 1.0rem 0;
      }
      .hero-actions { display: flex; gap: .6rem; flex-wrap: wrap; }

      /* Fake “polaroid” frame for hero image */
      .img-polaroid img {
        border-radius: 8px;
        background: #fff;
        box-shadow: 0 12px 22px rgba(0,0,0,.18);
        border: 10px solid #fff;
        transform: rotate(-3deg);
      }

      .divider { margin: 1.5rem 0 1.25rem 0; border: none; border-top: 1px solid rgba(0,0,0,.08); }
      .section-kicker {
        font-size: clamp(18px, 2.2vw, 22px);
        font-weight: 800;
        letter-spacing: .10em;
        text-transform: uppercase;
        color: #2a2a2a;
        margin: .25rem 0 1rem 0;
      }

      /* Cards */
      .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
      @media (max-width: 1000px) { .cards { grid-template-columns: 1fr; } }

      .card {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,.08);
        padding: 0.9rem 0.9rem 1.1rem 0.9rem;
        border: 1px solid rgba(0,0,0,.05);
      }
      .img-card img {
        width: 100%;
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,.12);
      }
      .card h4 { margin: .35rem 0 .3rem 0; font-size: 17px; }
      .card .sub { color: rgba(0,0,0,.6); font-size: 14px; margin-bottom: .55rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Image loader that ALWAYS works ------------------
def load_image_bytes(path_str: str) -> bytes | None:
    """
    Read an image file from disk, validate with PIL, and return raw bytes.
    Works reliably on Streamlit Cloud regardless of current working dir.
    """
    p = Path(path_str)
    if not p.exists():
        st.info(f"Add image at {path_str}")
        return None
    try:
        with p.open("rb") as f:
            data = f.read()
        # Validate it’s an actual image
        Image.open(io.BytesIO(data)).verify()
        return data
    except UnidentifiedImageError:
        st.warning(f"{p.name} exists but isn't a valid image file. Replace it with PNG/JPG/WEBP.")
    except Exception as e:
        st.warning(f"Couldn't load {p.name}: {e}")
    return None

def show_image_bytes(path: str, *, width: int | str = "stretch", wrapper_class: str | None = None):
    b = load_image_bytes(path)
    if not b:
        return
    if wrapper_class:
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
    st.image(b, width=width if isinstance(width, int) else width)
    if wrapper_class:
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ HERO ------------------
with st.container():
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)

    # Left: text
    st.markdown(
        """
        <div>
          <div class="hero-h1">YOUR COMPASSIONATE<br>GUIDE TO SENIOR<br>CARE DECISIONS</div>
          <div class="hero-h2">
            Every care decision matters. We’re here to guide you — at no cost —
            whether planning for yourself or a loved one.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Right: hero image (bytes → st.image), smaller to match your PDF
    show_image_bytes("static/images/Hero.png", width=380, wrapper_class="img-polaroid")
    st.markdown("</div>", unsafe_allow_html=True)

    # Buttons under text
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)

# ------------------ CARDS ------------------
st.markdown('<div class="cards">', unsafe_allow_html=True)

# Card 1
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    show_image_bytes("static/images/Someone-Else.png", width="stretch", wrapper_class="img-card")
    st.markdown("**I would like to support my loved ones**", unsafe_allow_html=True)
    st.markdown('<div class="sub">For someone</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_b:
        if st.button("For someone", key="tile_someone_btn"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Card 2
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    show_image_bytes("static/images/Myself.png", width="stretch", wrapper_class="img-card")
    st.markdown("**I’m looking for support just for myself**", unsafe_allow_html=True)
    st.markdown('<div class="sub">For myself</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns([1, 1])
    with col_d:
        if st.button("For myself", key="tile_myself_btn"):
            st.switch_page("pages/tell_us_about_you.py")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # end .cards
