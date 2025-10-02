# Handoff 1 — Audiencing Dev (Authoritative Contract)

Implements audience short-circuit flags and writes them to `st.session_state["audiencing"]`.
Exposes `get_audience()` on the page and `apply_audiencing_sanitizer(state)` in the library.

Contract:
- entry: self|proxy|pro
- qualifiers: is_veteran, has_partner, owns_home, on_medicaid, urgent
- route.next: guided_care_plan | medicaid_off_ramp | plan_for_my_advisor

Testing:
- No partner → household.mode == "single" and p2 removed.
- Not veteran → VA offsets zeroed.
- Not homeowner → home-mods/sell-home/utilities zeroed.
- On Medicaid → banner appears in UI.
