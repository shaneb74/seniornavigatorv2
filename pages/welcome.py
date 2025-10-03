"""Unified welcome screen with segmented entry selection."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    AUDIENCING_QUALIFIER_KEYS,
    apply_audiencing_sanitizer,
    compute_audiencing_route,
    ensure_audiencing_state,
    log_audiencing_set,
    snapshot_audiencing,
)

st.set_page_config(page_title="Welcome", layout="wide")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_defaults() -> None:
    state = ensure_audiencing_state()
    state.setdefault("entry", "proxy")
    qualifiers = state.setdefault("qualifiers", {})
    for key in AUDIENCING_QUALIFIER_KEYS:
        qualifiers.setdefault(key, False)
    state.setdefault("route", {"next": None})
    state.setdefault("recipient_name", None)
    state.setdefault("proxy_name", None)
    st.session_state.setdefault(
        "care_context",
        {
            "person_name": "Your Loved One",
            "gcp_answers": {},
            "gcp_recommendation": None,
            "gcp_cost": None,
        },
    )


def _apply_and_snapshot() -> None:
    aud = st.session_state["audiencing"]
    apply_audiencing_sanitizer(aud)
    compute_audiencing_route(aud)
    st.session_state["audiencing_snapshot"] = snapshot_audiencing(aud)


def _navigate(entry: str) -> None:
    if entry == "self":
        st.switch_page("pages/tell_us_about_you.py")
    elif entry == "proxy":
        st.switch_page("pages/tell_us_about_loved_one.py")
    else:
        log_audiencing_set(st.session_state.get("audiencing_snapshot", {}))
        st.switch_page("pages/hub.py")


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

_seed_defaults()
aud = st.session_state["audiencing"]
care_context = st.session_state["care_context"]

st.markdown("""
<div style="display:flex; flex-direction:column; gap:1.4rem;">
  <div>
    <h1 style="margin-bottom:0.6rem;">We’re here to help you find the support your loved ones need.</h1>
    <p style="font-size:1.05rem; color:#4b5563; max-width:640px;">
      Choose who you’re planning for to personalize the guidance, then take the next step in just a couple of minutes.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

segment_default = st.session_state.get("welcome_segment", "For someone")
st.markdown('<div class="sn-segmented">', unsafe_allow_html=True)
segment_choice = st.radio(
    "Audience selector",
    options=("For someone", "For me"),
    index=(0 if segment_default == "For someone" else 1),
    horizontal=True,
    label_visibility="collapsed",
    key="welcome_segment",
)
st.markdown("</div>", unsafe_allow_html=True)

entry = "proxy" if segment_choice == "For someone" else "self"
aud["entry"] = entry

if entry == "self":
    care_context["person_name"] = "You"
    prompt_label = "What’s your name?"
else:
    prompt_label = "What’s their name?"

if entry == "proxy":
    default_name = aud.get("recipient_name") or ""
else:
    default_name = care_context.get("person_name") if care_context.get("person_name") not in (None, "Your Loved One") else ""

col_field, col_cta = st.columns([4, 2], gap="large")
with col_field:
    person_name = st.text_input(
        prompt_label,
        value=default_name,
        placeholder="Add a name so we can personalize guidance",
        key="welcome_person_name",
    )
with col_cta:
    st.write("")
    st.write("")
    continue_clicked = st.button(
        "Continue",
        type="primary",
        use_container_width=True,
        key="welcome_continue",
    )

helper_note = "If you want to assess several people, don’t worry — you can easily move on to the next step!"
st.markdown(f'<div class="sn-helper-note">{helper_note}</div>', unsafe_allow_html=True)

pro_clicked = st.button(
    "I’m a professional", key="welcome_professional", type="secondary"
)

if continue_clicked:
    if entry == "proxy":
        aud["recipient_name"] = (person_name or "").strip() or None
        aud["proxy_name"] = None
        care_context["person_name"] = aud.get("recipient_name") or "Your Loved One"
    else:
        aud["recipient_name"] = None
        aud["proxy_name"] = None
        care_context["person_name"] = "You"
    _apply_and_snapshot()
    log_audiencing_set(st.session_state["audiencing_snapshot"])
    _navigate(entry)

if pro_clicked:
    aud["entry"] = "pro"
    for key in AUDIENCING_QUALIFIER_KEYS:
        aud["qualifiers"][key] = False
    care_context["person_name"] = "Your Loved One"
    _apply_and_snapshot()
    _navigate("pro")
