from __future__ import annotations

import base64
import io
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
from PIL import Image, UnidentifiedImageError


st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


def _switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.rerun()


def _resolve_path(path_str: str) -> Path:
    cand = Path(path_str)
    if cand.is_absolute():
        return cand
    here = Path(__file__).resolve().parent
    if cand.exists():
        return cand
    local = here / path_str
    if local.exists():
        return local
    return here.parent / path_str


@st.cache_data(show_spinner=False)
def _load_bytes(path_str: str) -> bytes | None:
    try:
        parsed = urlparse(path_str)
        if parsed.scheme in {"http", "https"}:
            import urllib.request

            with urllib.request.urlopen(path_str, timeout=10) as resp:
                data = resp.read()
        else:
            target = _resolve_path(path_str)
            if not target.exists():
                return None
            data = target.read_bytes()
        Image.open(io.BytesIO(data)).verify()
        return data
    except UnidentifiedImageError:
        return None
    except Exception:
        return None


def _image_tag(path_str: str, *, alt: str = "", style: str = "", cls: str = "") -> str | None:
    raw = _load_bytes(path_str)
    if not raw:
        return None
    suffix = Path(urlparse(path_str).path).suffix.lower()
    mime = mimetypes.types_map.get(suffix, "image/png")
    encoded = base64.b64encode(raw).decode("ascii")
    cls_attr = f' class="{cls}"' if cls else ""
    style_attr = f' style="{style}"' if style else ""
    alt_attr = f' alt="{alt}"' if alt else ' alt=""'
    return f'<img src="data:{mime};base64,{encoded}"{cls_attr}{style_attr}{alt_attr}>'


# ---------------- Hero ----------------
hero_left, hero_right = st.columns([7, 5], gap="large")

with hero_left:
    st.markdown("# Concierge Care Advisors")
    st.markdown("## Senior Navigator")
    st.write(
        "Expert advisors — no cost. We help families navigate senior living and care decisions with "
        "personalized guidance, local knowledge, and white-glove support."
    )
    st.markdown(
        """
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 22px;">
          <span style="background:rgba(11,92,216,0.12);border:1px solid rgba(11,92,216,0.24);
                       color:#0B5CD8;font-weight:600;font-size:14px;border-radius:999px;
                       padding:6px 14px;">
            Trusted by 20,000+ families
          </span>
          <span style="background:rgba(11,92,216,0.12);border:1px solid rgba(11,92,216,0.24);
                       color:#0B5CD8;font-weight:600;font-size:14px;border-radius:999px;
                       padding:6px 14px;">
            15 years of excellence
          </span>
          <span style="background:rgba(11,92,216,0.12);border:1px solid rgba(11,92,216,0.24);
                       color:#0B5CD8;font-weight:600;font-size:14px;border-radius:999px;
                       padding:6px 14px;">
            HIPAA-conscious & privacy-first
          </span>
          <span style="background:rgba(11,92,216,0.12);border:1px solid rgba(11,92,216,0.24);
                       color:#0B5CD8;font-weight:600;font-size:14px;border-radius:999px;
                       padding:6px 14px;">
            Real human guidance
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

hero_img = _image_tag(
    "static/images/Hero.png",
    alt="Advisor supporting an older adult",
    style="width:min(420px,100%);display:block;border-radius:12px;",
)
with hero_right:
    if hero_img:
        st.markdown(
            """
            <div style="background: radial-gradient(120% 120% at 80% 10%, #eef2ff 0%, #ffffff 60%);
                        padding: 18px; border-radius: 18px; box-shadow:0 10px 24px rgba(15,23,42,0.12);
                        border:10px solid #ffffff; transform:rotate(-1.5deg);">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(hero_img, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Add hero image at static/images/Hero.png to complete this section.")

st.markdown("---")


# ---------------- Who we are ----------------
st.subheader("Who we are")
st.write(
    "Concierge Care Advisors is a concierge advisory service guiding families through senior living and care choices. "
    "We coordinate the next steps—from tours and paperwork to benefit reviews and move-in logistics—and stay available even after placement."
)
st.markdown(
    """
    - Local, “boots-on-the-ground” expertise
    - No-cost guidance for families
    - Coordinated support with care, legal, and financial professionals
    - Transparent, family-first recommendations
    """
)


# ---------------- Mission & Values ----------------
st.subheader("Mission & values")
st.write(
    "Our mission is to deliver personalized, dignified support so every family can move forward with confidence throughout complex care decisions."
)

values = [
    ("🧭", "Independence", "Honor each person’s preferences, routines, and ideal lifestyle."),
    ("🤝", "Trust", "Offer clear, unbiased guidance grounded in your goals and safety."),
    ("🏥", "Quality", "Surface vetted options and keep safety and standards front and center."),
    ("🔄", "Follow-Through", "Provide ongoing support long after move-in day."),
]

val_cols = st.columns(2, gap="large")
for idx, (icon, title, description) in enumerate(values):
    with val_cols[idx % 2]:
        with st.container(border=True):
            st.markdown(f"**{icon} {title}**")
            st.write(description)


# ---------------- Why families choose us ----------------
st.subheader("Why families choose us")
reasons = [
    ("No cost for families", "Our guidance is always free to you—we’re here as your advocate."),
    (
        "Personalized choice",
        "We match recommendations to your needs, safety priorities, lifestyle, and budget.",
    ),
    ("Local expertise", "We know the communities, the staff, and the standards that matter."),
    (
        "White-glove support",
        "We coordinate tours, paperwork, benefits conversations, and follow-up details.",
    ),
]

for title, description in reasons:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(description)


# ---------------- Trust signals ----------------
st.subheader("Trust signals")
trust_cols = st.columns([1, 1], gap="large")

with trust_cols[0]:
    bbb_tag = _image_tag(
        "static/images/better-business-bureau-logo.png",
        alt="Better Business Bureau A+ Rating",
        style="width:160px;height:auto;display:block;margin:0 auto;",
    )
    if bbb_tag:
        st.markdown(bbb_tag, unsafe_allow_html=True)
        st.caption("A+ Rating")
    else:
        st.info("Add BBB logo at static/images/better-business-bureau-logo.png")

with trust_cols[1]:
    star_svg = (
        '<svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" '
        'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462'
        'c.969 0 1.371 1.24.588 1.81l-2.802 2.036a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755'
        ' 1.688-1.54 1.118l-2.802-2.036a1 1 0 00-1.175 0l-2.802 2.036c-.784.57-1.838-.197-1.539-1.118'
        'l1.07-3.292a1 1 0 00-.364-1.118L2.88 8.72c-.783-.57-.38-1.81.588-1.81H6.93a1 1 0 00.95-.69'
        'l1.169-3.292z"/></svg>'
    )
    stars = f'<span aria-label="5 out of 5 stars">{star_svg * 5}</span>'
    st.markdown(
        f"""
        <div style="background:#ffffff;border:1px solid rgba(15,23,42,0.12);border-radius:16px;
                   padding:1.1rem 1.3rem;box-shadow:0 12px 28px rgba(15,23,42,0.08);">
          <div style="color:#F59E0B;display:inline-flex;gap:2px;margin-bottom:.4rem;">{stars}</div>
          <div style="font-size:1rem;color:#1f2937;margin-bottom:.6rem;">
            “Our Advisor guided us with empathy and expertise—she made a difficult time feel manageable.”
          </div>
          <div style="font-size:.9rem;color:#64748B;font-weight:500;">Google review (example)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------- How we work ----------------
st.subheader("How we work")
steps = [
    ("Listen & learn", "We understand your goals, safety needs, and budget before making recommendations."),
    ("Curate options", "We match communities and services to your care profile and explain tradeoffs."),
    ("Coordinate next steps", "We arrange tours, outline paperwork, review benefits, and prepare timelines."),
    ("Follow through", "We stay connected after move-in with resources and ongoing check-ins."),
]

for index, (title, description) in enumerate(steps, start=1):
    with st.container(border=True):
        st.markdown(f"**Step {index}. {title}**")
        st.write(description)


# ---------------- Advisors & community ----------------
st.subheader("Advisors & community")
st.write("Our Advisors and clinical partners bring decades of regional experience.")
if st.button("Talk to an Advisor", key="about_us_talk", type="secondary"):
    _switch_page("app_pages/SeniorNav_welcome_professional.py")


# ---------------- CTA footer ----------------
st.markdown("---")
cta_cols = st.columns([1, 1, 1], gap="large")
with cta_cols[1]:
    if st.button("Begin Guided Care Plan", type="primary", use_container_width=True):
        _switch_page("app_pages/gcp_v2/gcp_landing_v2.py")
with cta_cols[2]:
    if st.button("Return to Care Hub", type="secondary", use_container_width=True):
        _switch_page("app_pages/hub.py")

st.markdown("</div>", unsafe_allow_html=True)
