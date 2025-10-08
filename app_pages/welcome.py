from __future__ import annotations

import base64
import io
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
from PIL import Image, UnidentifiedImageError

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# ------------------ Session scaffolding ------------------
if "care_context" not in st.session_state:
    st.session_state.care_context = {"person_name": "Your Loved One"}
if "aud" not in st.session_state:
    st.session_state.aud = {
        "entry": "proxy",
        "recipient_name": None,
        "proxy_name": None,
        "qualifiers": {},
    }

care_context = st.session_state.care_context
aud = st.session_state.aud

# ------------------ CSS ------------------
st.markdown(
    """
    <style>
      .block-container{
        max-width: 1120px;
        margin: 0 auto;
        padding-top: 1.25rem;
        padding-bottom: 3rem;
      }

      .hero-h1{
        font-size: clamp(32px, 4.2vw, 48px);
        line-height: 1.04;
        font-weight: 800;
        letter-spacing: -.01em;
        margin: 0 0 .35rem 0;
      }
      .hero-h2{
        font-size: clamp(16px, 1.85vw, 20px);
        color: rgba(15,23,42,0.82);
        font-weight: 600;
        margin: 0;
      }
      .hero-tagline{
        font-size: clamp(16px, 2vw, 20px);
        color: rgba(15,23,42,0.72);
        margin: .6rem 0 1.4rem;
      }

      .hero-chips{
        display:flex;
        gap:12px;
        flex-wrap:wrap;
        margin: 6px 0 22px 0;
      }
      .hero-chips span{
        background: rgba(11,92,216,0.12);
        border:1px solid rgba(11,92,216,0.26);
        color:#0B5CD8;
        border-radius:999px;
        padding:6px 14px;
        font-weight:600;
        font-size:14px;
        transition: background .15s ease, color .15s ease;
      }
      .hero-chips span:hover{
        background:#0B5CD8;
        color:#ffffff;
      }

      .hero-photo{
        border-radius: 10px;
        background:#fff;
        box-shadow: 0 10px 24px rgba(15,23,42,0.12);
        border: 10px solid #fff;
        transform: rotate(-1.8deg);
        display: block;
      }

      .divider{ margin: 1.25rem 0 1rem; border: none; border-top: 1px solid rgba(0,0,0,.08); }
      .section-kicker{
        font-size: clamp(18px, 2.2vw, 22px);
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #2a2a2a;
        margin: .25rem 0 1rem 0;
      }

      div[data-testid="stVerticalBlockBorderWrapper"]{
        border: 1px solid rgba(0,0,0,.06);
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,.08);
      }

      .card-photo{
        width: clamp(280px, 82%, 420px);
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,.12);
        display: block;
        margin: .35rem auto .8rem;
      }

      .sn-helper-note{
        margin-top: 1.2rem;
        text-align: center;
        font-size: 1.05rem;
        font-weight: 500;
        color: #0B5CD8;
        background: rgba(11,92,216,0.06);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        display: inline-block;
        max-width: 560px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
      }
      .sn-divider-note{
        margin: 0 auto;
        padding: .9rem 1.2rem;
        background:#F7FAFC;
        border:1px solid rgba(15,23,42,0.08);
        border-radius: 999px;
        font-size:1.02rem;
        font-weight:600;
        color:#0F172A;
        text-align:center;
        max-width: 520px;
      }

      .sn-row-badges {
        display:flex; gap:14px; align-items:center; flex-wrap:wrap; margin: 4px 0 22px 0;
      }
      .sn-bbb{
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        background:#fff;
        border:1px solid rgba(2,6,23,.06);
        border-radius:14px; padding:12px 14px;
        box-shadow:0 8px 24px rgba(0,0,0,.04);
        min-width:140px;
      }
      .sn-bbb img{max-width:120px; height:auto;}
      .sn-bbb .meta{margin-top:6px; font-size:.85rem; color:#334155; font-weight:600;}
      .sn-review {
        display:flex; gap:12px; align-items:flex-start;
        background:#fff;
        border:1px solid rgba(2,6,23,.06);
        border-radius:14px; padding:12px 14px;
        box-shadow:0 8px 24px rgba(0,0,0,.06);
        max-width:780px;
      }
      .sn-review .avatar {
        flex:0 0 auto; width:40px; height:40px; border-radius:999px; overflow:hidden;
        background:#EEF2FF; display:flex; align-items:center; justify-content:center;
        font-weight:700; color:#0B5CD8; border:1px solid rgba(2,6,23,.06);
      }
      .sn-review .body { flex:1 1 auto; }
      .sn-review .meta {
        display:flex; align-items:center; gap:8px; margin-bottom:4px;
        font-size:.92rem; color:#334155; font-weight:600;
      }
      .sn-review .stars { display:inline-flex; gap:2px; line-height:0; color:#F59E0B; }
      .sn-review .source { font-size:.82rem; color:#64748B; font-weight:500; }
      .sn-review .quote { font-size:.95rem; color:#1F2937; }
      .sn-review-simple{
        background:#ffffff;
        border:1px solid rgba(2,6,23,.08);
        border-radius:16px;
        padding:1.2rem 1.4rem;
        box-shadow:0 12px 28px rgba(15,23,42,0.08);
        max-width:640px;
      }
      .sn-review-label{
        font-size:.9rem;
        text-transform:uppercase;
        letter-spacing:.12em;
        color:#475569;
        font-weight:600;
        margin-bottom:.4rem;
      }
      .sn-review-stars{
        font-size:1.1rem;
        color:#F59E0B;
        margin-bottom:.4rem;
        display:inline-block;
      }
      .sn-review-quote{
        font-size:1rem;
        color:#1F2937;
        margin-bottom:.6rem;
      }
      .sn-review-source{
        font-size:.9rem;
        color:#64748B;
        font-weight:500;
      }

      .sn-pro-icons{
        display:flex;
        flex-direction:column;
        gap:.45rem;
        margin:.9rem 0 1.3rem;
        font-size:.95rem;
        color:#1f2937;
      }
      .sn-pro-block{
        background:#ffffff;
        border:1px solid rgba(15,23,42,0.08);
        border-radius:20px;
        padding:2.4rem 2rem;
        box-shadow:0 18px 38px rgba(15,23,42,0.08);
        max-width:760px;
        margin:0 auto;
        text-align:center;
      }
      .sn-pro-block h3{
        margin:0 0 .5rem 0;
        font-size:1.45rem;
      }
      .sn-pro-block p{
        margin:0 0 1.1rem 0;
        color:#1f2937;
        font-size:1.02rem;
      }

      div[data-testid="stMarkdownContainer"]:empty{ display:none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Image helpers ------------------
def _resolve_path(path_str: str) -> Path:
    p = Path(path_str)
    if p.is_absolute() or p.exists():
        return p
    here = Path(__file__).resolve().parent
    cand = here / path_str
    if cand.exists():
        return cand
    root = here.parents[1] if len(here.parents) > 1 else here.parent
    return root / path_str


@st.cache_data(show_spinner=False)
def load_bytes(path_str: str) -> bytes | None:
    try:
        parsed = urlparse(path_str)
        if parsed.scheme in ("http", "https"):
            import urllib.request

            with urllib.request.urlopen(path_str, timeout=10) as r:
                data = r.read()
        else:
            p = _resolve_path(path_str)
            if not p.exists():
                return None
            data = p.read_bytes()
        Image.open(io.BytesIO(data)).verify()
        return data
    except UnidentifiedImageError:
        return None
    except Exception:
        return None


def data_uri(path_str: str) -> str | None:
    raw = load_bytes(path_str)
    if not raw:
        return None
    ext = Path(urlparse(path_str).path).suffix.lower()
    mime = mimetypes.types_map.get(ext, "image/png")
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def img_html(path_str: str, *, cls: str = "", style: str = "", alt: str = "") -> str | None:
    uri = data_uri(path_str)
    if not uri:
        return None
    cls_attr = f' class="{cls}"' if cls else ""
    style_attr = f' style="{style}"' if style else ""
    alt_attr = f' alt="{alt}"' if alt else ' alt=""'
    return f'<img src="{uri}"{cls_attr}{style_attr}{alt_attr}>'


# ------------------ Navigation helper ------------------
def safe_switch_page(target: str, query_key: str | None = None, query_value: str | None = None) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        if query_key and query_value:
            st.query_params[query_key] = query_value
        st.rerun()


# ------------------ Hero ------------------
top_cols = st.columns([6, 2])
with top_cols[1]:
    login_placeholder = st.container()
    with login_placeholder:
        if st.button("Log in", type="secondary", use_container_width=True, key="welcome_login_top"):
            safe_switch_page("app_pages/SeniorNav_login.py", "view", "login")

left, right = st.columns([7, 5], gap="large")

with left:
    st.markdown(
        """
        <div class="hero-h1">Concierge Care Advisors</div>
        <div class="hero-h2">Senior Navigator</div>
        <div class="hero-tagline">Expert advisors — no cost. Helping families navigate the most important senior living decisions with clarity and compassion.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="hero-chips">
          <span>15 years of excellence</span>
          <span>20,000+ families served</span>
          <span>Real human advisors</span>
          <span>No cost, ever</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("More About Us", type="primary", use_container_width=False):
        safe_switch_page("app_pages/about_us.py")

with right:
    hero_tag = img_html(
        "static/images/Hero.png",
        cls="hero-photo",
        style="width:min(420px, 100%);",
        alt="Caregiver smiling with older adult",
    )
    if hero_tag:
        st.markdown(
            """
            <div style="background: radial-gradient(120% 120% at 80% 10%, #eef2ff 0%, #ffffff 60%);
                        padding: 18px; border-radius: 18px;">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(hero_tag, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

bbb_html = img_html(
    "static/images/better-business-bureau-logo.png",
    style="width:120px;height:auto;",
    alt="Better Business Bureau A+ Rating badge",
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="sn-divider-note" role="note" aria-label="Trusted by families">
      Trusted by over 20,000 families — guided with care and clarity.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)


# ------------------ CTA cards ------------------
def card(image_path: str, title: str, subtitle: str, body: str, button_label: str, page_to: str) -> None:
    with st.container(border=True):
        img_tag = img_html(image_path, cls="card-photo", alt=title)
        if img_tag:
            st.markdown(img_tag, unsafe_allow_html=True)
        st.markdown(f"**{title}**")
        if subtitle:
            st.caption(subtitle)
        if body:
            st.write(body)
        if st.button(button_label, key=f"btn_{page_to}", type="primary", use_container_width=True):
            safe_switch_page(page_to, "view", "open")


card_cols = st.columns(2, gap="large")
with card_cols[0]:
    card(
        "static/images/Someone-Else.png",
        "Supporting Others",
        "For a loved one",
        "Helping you make confident care decisions for someone you love.",
        "For someone",
        "app_pages/SeniorNav_welcome_someone_else.py",
    )
with card_cols[1]:
    card(
        "static/images/Self.png",
        "Getting Ready for Myself",
        "For myself",
        "Plan for your own future care with trusted guidance and peace of mind.",
        "For me",
        "app_pages/SeniorNav_welcome_self.py",
    )

helper_note = (
    "Supporting more than one person? No problem—you can add another anytime in your cost planner or care hub."
)
st.markdown(f'<div class="sn-helper-note">{helper_note}</div>', unsafe_allow_html=True)


# ------------------ Trust signals ------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
trust_cols = st.columns([1, 1], gap="large")

with trust_cols[0]:
    st.markdown(
        """
        <div class="sn-review-simple">
          <div class="sn-review-label">What families say</div>
          <div class="sn-review-stars" role="img" aria-label="5 out of 5 stars">★★★★★</div>
          <div class="sn-review-quote">“Our advisor made a complicated process feel simple, supportive, and personal.”</div>
          <div class="sn-review-source">— Verified Google Review</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with trust_cols[1]:
    if bbb_html:
        st.markdown(
            f"""
            <div class="sn-review-simple" style="text-align:center;">
              <div style="margin-bottom:.5rem;">{bbb_html}</div>
              <div class="sn-review-source">A+ Rating — 15 Years of Excellence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Add BBB logo image at static/images/better-business-bureau-logo.png")

# ------------------ Professional block ------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="sn-pro-block">
      <div style="font-size:2rem; margin-bottom:.75rem;">💼</div>
      <h3>Are you a discharge planner, hospital partner, or professional advisor?</h3>
      <p>Learn how we work with professionals to make safe transitions easier.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
pro_cta_col = st.columns([1, 1, 1])[1]
with pro_cta_col:
    if st.button("For Professionals", type="primary", key="welcome_professional"):
        safe_switch_page("app_pages/SeniorNav_professional_hub.py")


# ------------------ Legacy actions ------------------
if "continue_clicked" in locals() and continue_clicked:
    if aud.get("entry") == "proxy":
        aud["recipient_name"] = (aud.get("recipient_name") or "").strip() or None
        aud["proxy_name"] = None
        care_context["person_name"] = aud.get("recipient_name") or "Your Loved One"
        safe_switch_page("app_pages/SeniorNav_welcome_someone_else.py")
    elif aud.get("entry") == "self":
        care_context["person_name"] = "You"
        safe_switch_page("app_pages/SeniorNav_welcome_self.py")
    else:
        safe_switch_page("app_pages/SeniorNav_welcome_someone_else.py")
