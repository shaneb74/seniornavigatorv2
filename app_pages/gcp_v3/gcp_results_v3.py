from ui.theme import inject_theme
inject_theme()

import streamlit as st

# ---------- Wrapper ----------
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

st.title("Your Guided Care Plan Results")

# Pull state
answers = st.session_state.get("gcp_v3.answers", {})
flags = set(st.session_state.get("gcp_v3.flags", set()))
medicaid_status = st.session_state.get("medicaid_status")

# Try to use your core modules if available; otherwise fall back to a simple heuristic
tier = None
narrative_lines = []
highlights = []

try:
    from gcp_core.v3_scoring import score_domains, determine_tier
    from gcp_core.v3_blurbs import pick_blurbs_variant3
    from gcp_core.v3_summary_rules import final_summary_sentence

    domain_scores = score_domains(answers, flags)
    tier = determine_tier(domain_scores, answers, flags)
    blurbs = pick_blurbs_variant3(domain_scores, answers, flags)
    narrative_lines = blurbs
    narrative_lines.append(final_summary_sentence(domain_scores, answers, flags))

except Exception:
    # --- Simple heuristic fallback (keeps UI working while you wire CSV logic) ---
    # Compute a rough tier from a few key signals
    tier_score = 0
    cog = answers.get("cognitive")
    if cog in {"Moderate", "Severe"}:
        tier_score += 2
    if "behavior_risk" in flags:
        tier_score += 1
    if int(answers.get("falls_6mo") or 0) >= 2:
        tier_score += 1
    badls = answers.get("badls") or []
    iadls = answers.get("iadls") or []
    if len(badls) >= 2:
        tier_score += 1
    if len(iadls) >= 3:
        tier_score += 1
    if answers.get("mood") == "Low":
        tier_score += 1

    if tier_score <= 0:
        tier = 0
    elif tier_score == 1:
        tier = 1
    elif tier_score in {2, 3}:
        tier = 2
    elif tier_score in {4, 5}:
        tier = 3
    else:
        tier = 4

    # Narrative (one sentence per domain + wrap-up)
    oh = answers.get("overall_help")
    narrative_lines.append(
        f"Day-to-day support is '{oh}' with BADLs {', '.join(badls) or 'none'} and IADLs {', '.join(iadls) or 'none'}."
    )
    cognitive_line = f"Cognitive status is {cog or 'unspecified'}"
    if "behavior_risk" in flags:
        br = ", ".join(answers.get("behavior_risks") or [])
        cognitive_line += f" with behavior risks ({br})."
    else:
        cognitive_line += "."
    narrative_lines.append(cognitive_line)

    meds = answers.get("med_profile") or "unspecified"
    narrative_lines.append(f"Medication profile is {meds}.")
    mobility = answers.get("mobility") or "unspecified"
    falls = int(answers.get("falls_6mo") or 0)
    narrative_lines.append(f"Mobility is {mobility} with {falls} fall(s) in the last 6 months.")
    chronic = answers.get("chronic_conditions") or []
    mgmt = answers.get("mgmt_quality") or "unspecified"
    if len(chronic) >= 1:
        narrative_lines.append(f"Chronic conditions: {', '.join(chronic)} (management: {mgmt}).")
    mood = answers.get("mood") or "unspecified"
    narrative_lines.append(f"Mood is {mood}.")
    geo = answers.get("geo_isolation") or "unspecified"
    narrative_lines.append(f"Geographic isolation: {geo}.")
    narrative_lines.append("Overall, the above suggests the level of care below while balancing independence and safety.")

# Highlights
if (answers.get("overall_help") in {"Regular", "Extensive"}) or (len(answers.get("badls") or []) >= 2):
    highlights.append("Needs regular support with daily activities.")
if "behavior_risk" in flags or (answers.get("cognitive") in {"Moderate", "Severe"}):
    highlights.append("Cognitive safety risks present; structured setting may help.")
if int(answers.get("falls_6mo") or 0) >= 2:
    highlights.append("Recent falls indicate elevated safety risk.")
if (len(answers.get("chronic_conditions") or []) >= 2):
    highlights.append("Multiple chronic conditions; consistent care coordination recommended.")
if answers.get("mood") == "Low":
    highlights.append("Low mood noted; consider evaluation and supportive engagement.")
if "geo_isolated" in flags:
    highlights.append("Geographic isolation; plan for reliable support access.")

# Display
st.subheader("Recommendation")
st.write(f"**Suggested tier:** {tier}  \n(0 = none/nudge, 1 = in-home, 2 = assisted, 3 = memory, 4 = high-acuity memory)")

st.subheader("Summary")
for line in narrative_lines:
    st.write("• " + line)

if highlights:
    st.subheader("Highlights")
    for h in highlights:
        st.write("• " + h)

st.divider()

# ---------- CTAs ----------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Continue to Cost Planner", type="primary"):
        try:
            st.switch_page("app_pages/cost_planner_v2/cost_planner_landing_v2.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/cost_planner_v2/cost_planner_landing_v2.py"
            st.rerun()

with col2:
    if st.button("Return to Care Hub"):
        try:
            st.switch_page("app_pages/hub.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/hub.py"
            st.rerun()

with col3:
    # Show if risk/complexity or mood "Low"
    show_advisor = ("behavior_risk" in flags) or (answers.get("mood") == "Low") or (tier and tier >= 2)
    if st.button("Talk to an Advisor", disabled=not show_advisor):
        # Hook up to your existing advisor flow if different
        try:
            st.switch_page("app_pages/pfma.py")
        except Exception:
            st.session_state["_target_page"] = "app_pages/pfma.py"
            st.rerun()

# Mark completion for hub chip
st.session_state["gcp_v3.completed"] = True
st.session_state["gcp_v3.scorecard"] = {"tier": tier}

st.markdown("</div>", unsafe_allow_html=True)