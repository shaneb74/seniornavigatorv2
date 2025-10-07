"""Plan for My Advisor · Booking screen."""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from types import SimpleNamespace

import streamlit as st

from ui.theme import inject_theme

inject_theme()

from ui.pfma import (

#Production Page

apply_pfma_theme,
    ensure_date,
    ensure_pfma_state,
    go_to_step,
    mark_step_complete,
    render_header,
    render_progress,
    segmented_control,
    set_badges_from_progress,
)

RELATIONSHIP_OPTIONS = (
    "Self",
    "Spouse",
    "Adult child",
    "Sibling",
    "Friend",
    "Professional",
)

AGE_BANDS = ("<65", "65-74", "75-84", "85+")

URGENCY_OPTIONS = (
    "Exploring options",
    "Soon",
    "Ready this week",
    "ASAP",
)

TIME_SLOTS = ("Morning", "Midday", "Afternoon", "Evening")

PHONE_PATTERN = re.compile(r"^\d{10}$")

def _init_field(key: str, default: str | None = "") -> str:
    session_key = f"pfma_booking_{key}"
    booking = ensure_pfma_state()["booking"]
    if session_key not in st.session_state:
        st.session_state[session_key] = booking.get(key, default)
    return session_key

def _format_phone(digits: str) -> str:
    if len(digits) != 10:
        return digits
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

def _as_date(v) -> date | None:
    """Coerce assorted values into a datetime.date or return None."""
    if isinstance(v, date):
        return v
    if isinstance(v, SimpleNamespace):
        v = getattr(v, "date", None)
        if isinstance(v, date):
            return v
    if isinstance(v, str) and v:
        try:
            return datetime.fromisoformat(v).date()
        except Exception:
            for fmt in ("%m/%d/%Y", "%m/%d/%y"):
                try:
                    return datetime.strptime(v, fmt).date()
                except Exception:
                    pass
    return None

apply_pfma_theme()
state = ensure_pfma_state()

render_header("Step 1 · Booking your concierge call")
render_progress("booking")

if st.sidebar.checkbox("Ask Advisor", key="pfma_booking_sidebar", help="Curious why we ask for these details?"):
    st.sidebar.info("Sharing contact basics lets your concierge prep confirmations and respect your timing preferences.")

why_key = "pfma_booking_why"
if why_key not in st.session_state:
    st.session_state[why_key] = False
if st.button("Why this step?", key="pfma_booking_why_button"):
    st.session_state[why_key] = not st.session_state[why_key]
if st.session_state[why_key]:
    st.info("Capturing booking details now means no back-and-forth later-your concierge arrives ready with next steps.")

booking = state["booking"]
urgency_value = booking.get("urgency")
if urgency_value in {"Ready this week", "ASAP"}:
    st.markdown(
        """<div class='pfma-banner'>You’ve marked this as urgent — we’ll prioritize your call.</div>""",
        unsafe_allow_html=True,
    )

left, right = st.columns([0.9, 1.4], gap="large")

with left:
    st.markdown(
        """
        <div class="pfma-card" style="background:linear-gradient(145deg, rgba(0,87,184,0.08) 0%, rgba(0,87,184,0) 60%),
             linear-gradient(110deg, rgba(251,192,45,0.15) 0%, rgba(255,255,255,0) 70%);">
          <span class="pfma-badge">Concierge on deck</span>
          <h3>Your personal advisor will call within 24 hours!</h3>
          <p>Lock in a time that works best for you. If anything changes, you can update details right up until the call.</p>
          <div style="display:flex;flex-direction:column;gap:.5rem;margin-top:.6rem;">
            <div style="display:flex;align-items:center;gap:.45rem;font-weight:600;color:#0b3e91;">
              <span>📞</span> <span>We'll text and email a confirmation instantly.</span>
            </div>
            <div style="display:flex;align-items:center;gap:.45rem;color:var(--ink-muted);">
              <span>🕑</span> <span>Need to reschedule? Reply to the confirmation or hop back here.</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<div class="pfma-card">', unsafe_allow_html=True)
    st.markdown(
        "<h3>Schedule your concierge call</h3><p style='margin:0;color:var(--ink-muted);'>Fill in the essentials so we can prep your advisor and send confirmations to the right place.</p>",
        unsafe_allow_html=True,
    )

    name_key = _init_field("name")
    relationship_default = booking.get("relationship")
    phone_key = _init_field("phone")
    email_key = _init_field("email")
    zip_key = _init_field("zip")
    notes_key = _init_field("notes")
    referral_key = _init_field("referral_source")

    st.markdown('<div class="pfma-fieldstack">', unsafe_allow_html=True)
    st.text_input("Full name", key=name_key, max_chars=100, placeholder="Jordan Rivera")

    segmented_control(
        "Relationship to the person receiving care",
        RELATIONSHIP_OPTIONS,
        key="relationship",
        default=relationship_default,
    )

    st.text_input("Best phone number", key=phone_key, max_chars=14, placeholder="(555) 867-5309")
    digits = re.sub(r"\D", "", st.session_state.get(phone_key, ""))
    if digits and not PHONE_PATTERN.match(digits):
        st.caption("Enter a 10-digit number so we can confirm by text.")

    st.text_input("Email address (optional)", key=email_key, max_chars=120, placeholder="you@example.com")

    st.text_input("ZIP Code", key=zip_key, max_chars=5, placeholder="94107")

    segmented_control("Age band", AGE_BANDS, key="age_band", default=booking.get("age_band"))

    segmented_control("Urgency", URGENCY_OPTIONS, key="urgency", default=urgency_value)

    segmented_control("Preferred time of day", TIME_SLOTS, key="time_slot", default=booking.get("time_slot"))

    # --- Preferred date (robust) ---
    min_date = date.today() + timedelta(days=1)
    raw = booking.get("preferred_date")

    # Try shared helper, then local coercion
    stored_date = ensure_date(raw) or _as_date(raw)

    if not isinstance(stored_date, date):
        stored_date = min_date
    elif stored_date < min_date:
        stored_date = min_date

    st.date_input(
        "Preferred date",
        key="pfma_booking_preferred_date",
        min_value=min_date,
        value=stored_date,
        help="You can always reschedule from the confirmation message.",
    )

    st.text_area("Notes for your advisor", key=notes_key, max_chars=500, height=120)
    st.text_input("Referral source (optional)", key=referral_key, max_chars=200, placeholder="Hospital discharge planner")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

errors_placeholder = st.empty()

st.markdown('<div class="pfma-sticky-nav">', unsafe_allow_html=True)
st.markdown('<div class="pfma-nav-inner">', unsafe_allow_html=True)
st.markdown(
    "<div class='pfma-note'>You can revisit any section from the hub to keep details fresh.</div>",
    unsafe_allow_html=True,
)

submit = st.button("Confirm booking", type="primary", key="pfma_booking_submit")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if submit:
    name_value = (st.session_state.get(name_key) or "").strip()
    relationship_value = st.session_state.get("pfma_segment_relationship")
    phone_digits = re.sub(r"\D", "", st.session_state.get(phone_key, ""))
    email_value = (st.session_state.get(email_key) or "").strip()
    zip_value = (st.session_state.get(zip_key) or "").strip()
    age_value = st.session_state.get("pfma_segment_age_band")
    urgency = st.session_state.get("pfma_segment_urgency")
    time_slot = st.session_state.get("pfma_segment_time_slot")
    preferred_date = st.session_state.get("pfma_booking_preferred_date")
    notes_value = (st.session_state.get(notes_key) or "").strip()
    referral_value = (st.session_state.get(referral_key) or "").strip()

    errors: list[str] = []
    if not name_value:
        errors.append("Add the contact name for the call.")
    if not relationship_value:
        errors.append("Select how you're connected.")
    if not phone_digits or not PHONE_PATTERN.match(phone_digits):
        errors.append("Enter a 10-digit phone number so we can confirm details by text.")
    if zip_value and not zip_value.isdigit():
        errors.append("ZIP code should be numbers only.")
    if not zip_value or len(zip_value) != 5:
        errors.append("Add a 5-digit ZIP code.")
    if age_value is None:
        errors.append("Choose an age band.")
    if urgency is None:
        errors.append("Let us know how urgent this is.")
    if time_slot is None:
        errors.append("Pick a preferred time of day.")
    if not isinstance(preferred_date, date) or preferred_date < (date.today() + timedelta(days=1)):
        errors.append("Select a date at least a day in the future.")
    if email_value and "@" not in email_value:
        errors.append("Email looks off-double-check for typos.")

    if errors:
        errors_placeholder.error("\n".join(errors))
    else:
        formatted_phone = _format_phone(phone_digits)
        booking_payload = {
            "name": name_value,
            "relationship": relationship_value,
            "phone": formatted_phone,
            "phone_digits": phone_digits,
            "email": email_value,
            "zip": zip_value,
            "age_band": age_value,
            "urgency": urgency,
            "time_slot": time_slot,
            "preferred_date": preferred_date.isoformat() if isinstance(preferred_date, date) else None,
            "notes": notes_value,
            "referral_source": referral_value,
        }
        state["booking"] = booking_payload
        dossier = st.session_state.setdefault("dossier", {})
        dossier.setdefault("pfma", {})["booking"] = booking_payload
        mark_step_complete("booking")
        set_badges_from_progress()
        st.toast("Booking confirmed. Your concierge will call within 24 hours.")
        if phone_digits:
            st.toast(f"Text sent to {formatted_phone}: Appointment confirmed.")
        go_to_step("care_plan")
