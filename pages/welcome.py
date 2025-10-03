# pages/welcome.py
import io
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

# ------------------ Page / session ------------------
st.set_page_config(layout="wide")

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
        font-size: clamp(26px, 3.6vw, 40px);
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
      .sn-card {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,.08);
        padding: 0.9rem 0.9rem 1.1rem 0.9rem;
        border: 1px solid rgba(0,0,0,.05);
      }
      .sn-photo img {
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,.12);
        display: block;
      }
      /* Hero photo “polaroid” look */
      .img-polaroid img {
        border-radius: 8px;
        background: #fff;
        box-shadow: 0 12px 22px rgba(0,0,0,.18);
        border: 10px solid #fff;
        transform: rotate(-3deg);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Image loader (reliable on Cloud) ------------------
def load_bytes(path_str: str) -> bytes | None:
    """
    Read image as bytes and validate with PIL.
    Works regardless of working directory or URL routing.
    """
    p = Path(path_str)
    if not p.exists():
        st.info(f"Add image at {path_str}")
        return None
    try:
        data = p.read_bytes()
        Image.open(io.BytesIO(data)).verify()
        return data
    except UnidentifiedImageError:
        st.warning(f"{p.name} exists but isn't a valid image file. Use PNG/JPG/WEBP.")
    except Exception as e:
        st.warning(f"Couldn't load {p.name}: {e}")
    return None

# ------------------ Card helper ------------------
def card(image_path: str, title: str, sub: str, button_label: str, page_to: str):
    with st.container():
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)

        b = load_bytes(image_path)
        if b:
            # Explicit width so images never render tiny
            st.markdown('<div class="sn-photo">', unsafe_allow_html=True)
            st.image(b, width=520)   # adjust if you want larger/smaller
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"**{title}**")
        st.caption(sub)
        _, right = st.columns([1, 1])
        with right:
            if st.button(button_label, key=f"btn_{page_to}"):
                st.switch_page(page_to)
        st.markdown('</div>', unsafe_allow_html=True)

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

    # Right: hero image (bytes → st.image) with explicit width
    hero_b = load_bytes("static/images/Hero.png")
    if hero_b:
        st.markdown('<div class="img-polaroid">', unsafe_allow_html=True)
        st.image(hero_b, width=420)  # adjust to taste
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Buttons under text (native Streamlit)
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")

# ------------------ CARDS ------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    card(
        "static/images/Someone-Else.png",
        "I would like to support my loved ones",
        "For someone",
        "For someone",
        "pages/tell_us_about_loved_one.py",
    )
with col2:
    card(
        "static/images/Myself.png",
        "I’m looking for support just for myself",
        "For myself",
        "For myself",
        "pages/tell_us_about_you.py",
    )
            st.switch_page("pages/tell_us_about_you.py")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # end .cards
