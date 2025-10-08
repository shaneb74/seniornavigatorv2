# Waiting Room Partner Spotlight stub
from __future__ import annotations

import streamlit as st


PARTNERS = [
    {"name": "BrightPath Care Advisors", "blurb": "RN-led guidance for comparing senior care communities.", "url": "https://example.com"},
    {"name": "SafeStep Home Mods", "blurb": "Certified aging-in-place contractors for home updates.", "url": "https://example.com"},
    {"name": "Harborway Financial", "blurb": "Funding specialists for long-term care and VA benefits.", "url": "https://example.com"},
    {"name": "Neighborhood Support Network", "blurb": "Volunteer respite, transport, and meal coordination.", "url": "https://example.com"},
]


def render() -> None:
    st.title("Waiting Room · Partner Spotlight")
    st.write("Explore trusted partners. Tap a card to learn more.")

    if not PARTNERS:
        st.info("Partner profiles are coming soon.")
    else:
        cols = st.columns(2)
        for idx, partner in enumerate(PARTNERS):
            column = cols[idx % len(cols)]
            with column:
                st.markdown(
                    f"""
                    <div class="sn-card">
                      <div class="sn-card-header">
                        <div class="sn-card-heading">
                          <h3 class="sn-card-title">{partner['name']}</h3>
                        </div>
                      </div>
                      <div class="sn-card-body">
                        <p>{partner['blurb']}</p>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("Learn more", partner["url"], type="secondary")

    if st.button("Back to Waiting Room", type="secondary"):
        try:
            st.switch_page("app_pages/SeniorNav_waiting_room.py")  # type: ignore[attr-defined]
        except Exception:
            st.session_state["nav_target"] = "app_pages/SeniorNav_waiting_room.py"
            st.rerun()


render()
