
import json, csv, os, hashlib
from typing import Dict, Tuple
from senior_nav.lib.trace import trace

PACKAGE_DIR = os.path.dirname(__file__)

# Cache loads
QUESTIONS_CSV = os.path.join(PACKAGE_DIR, "questions", "questions.csv")
SCORING_JSON  = os.path.join(PACKAGE_DIR, "scoring_model.json")
BLURBS_JSON   = os.path.join(PACKAGE_DIR, "blurbs", "context_blurbs.json")

def _load_questions():
    rows = list(csv.DictReader(open(QUESTIONS_CSV, "r", encoding="utf-8")))
    order, grouped = [], {}
    for r in rows:
        qid = r["id"]
        if qid not in grouped:
            grouped[qid] = {"id": qid, "label": r["label"], "type": r["type"], "choices": [] , "conditional_show": r.get("conditional_show","")}
            order.append(qid)
        grouped[qid]["choices"].append({"id": r["choice_id"], "label": r["choice_label"]})
    return [grouped[i] for i in order]

def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

QUESTIONS = _load_questions()
SC = _load_json(SCORING_JSON)
BLURBS = _load_json(BLURBS_JSON)

def _clamp01(x): return max(0.0, min(1.0, float(x)))

def evaluate_guided_care(answers: Dict, aud: Dict) -> Tuple[Dict, Dict]:
    # --- derive payment context precedence
    payment_context = "private"
    route = None
    medicaid_status = answers.get("medicaid_status")
    if medicaid_status == "yes":
        payment_context = "medicaid"; route = "medicaid_offramp"
    elif aud.get("on_medicaid"):
        payment_context = "medicaid"
    funding_conf = answers.get("funding_confidence", "unsure")
    medicaid_unsure_flag = (medicaid_status == "unsure")

    # enc helpers
    E = SC["encodings"]; HCM = SC["hc_component_maps"]
    def enc(table, key): return E[table].get(key, 0.0)

    # input pulls
    cog = answers.get("cognition","normal")
    adl = answers.get("adl_help","0-1")
    meds = answers.get("med_mgmt","simple")
    fall = answers.get("falls","none")
    home = answers.get("home_safety","safe")
    mob  = answers.get("mobility","no_issues")
    sup  = answers.get("supervision","always")
    iso  = answers.get("social_isolation","daily_or_often")
    acc  = answers.get("geographic_access","easy")
    support = answers.get("caregiver_support","none")
    behav_list = answers.get("behavior_risks") or []
    behav_val = "none"
    for b in ["exit_seeking","wandering","agitation"]:
        if b in behav_list:
            behav_val = b; break

    # compute bands
    MC = (0.45*enc("cognition",cog) + 0.20*enc("adl",adl) + 0.15*enc("meds",meds) +
          0.10*enc("home",home) + 0.07*enc("falls",fall) + 0.03*max(0.0, enc("support_penalty",support)) +
          0.10*min(enc("behav",behav_val), 1.2))
    AL = (0.35*enc("adl",adl) + 0.20*enc("isolation",iso) + 0.15*max(0.0, -enc("support_penalty",support)) +
          0.15*enc("home",home) + 0.10*enc("mobility",mob) + 0.05*min(enc("cognition",cog), 0.6) +
          0.05*enc("access",acc))

    HC_raw = (1.5
              - HCM["adl_map"][adl]
              - HCM["cog_map"][cog]
              - HCM["meds_map"][meds]
              + E["support_gain"][support]
              + HCM["home_gain"][home]
              - HCM["fall_sub"][fall]
              - HCM["iso_sub"][iso]
              - HCM["access_sub"][acc]
              - HCM["mob_sub"][mob])
    HC = _clamp01((HC_raw + 1.0) / 3.0)
    HC = _clamp01(HC + E["supervision_bias_HC"][sup])

    trace_lines = []

    # Bias rules
    al_bias = False
    if (home == "unsafe") or (fall in {"one","recurrent"} and support in {"few_days_week","none"}):
        AL = _clamp01(AL + 0.25); al_bias = True; trace_lines.append("Safety bias: home/fall/support → +0.25 AL")
    if (iso in {"rarely","almost_never"}) and (support in {"few_days_week","none"}):
        AL = _clamp01(AL + 0.15); al_bias = True; trace_lines.append("Isolation bias: +0.15 AL")

    # Hard stop
    hard_stop = (cog == "severe" and (adl in {"4-5","6+"} or meds=="complex" or home=="unsafe" or behav_val in {"wandering","exit_seeking"}))
    exception_ok = (sup in {"always","sometimes"}) and home != "unsafe"
    if hard_stop and not exception_ok:
        rec = "Memory Care"
        decision_id = "gcp.rec.memory.wandering_dementia"
    else:
        # final decision
        if MC >= 0.85:
            rec = "Memory Care"; decision_id = "gcp.rec.memory.high_score"
        else:
            if abs(HC-AL) <= 0.10:
                rec = "Assisted Living" if al_bias else ("In-Home Care" if HC >= AL else "Assisted Living")
            else:
                rec = "In-Home Care" if HC >= AL else "Assisted Living"
            decision_id = "gcp.rec.assisted.safety_supervision" if rec=="Assisted Living" else "gcp.rec.home.viable_support"

    # Build gcp
    gcp = {
        "recommended_setting": {"In-Home Care":"home","Assisted Living":"assisted","Memory Care":"memory"}.get(rec, "none"),
        "care_intensity": "high" if rec=="Memory Care" else ("med" if rec=="Assisted Living" else "low"),
        "safety_flags": {
            "falls": fall in {"one","recurrent"},
            "wandering": "wandering" in behav_list or "exit_seeking" in behav_list,
            "med_mgmt": meds in {"several","complex"}
        },
        "chronic_conditions": [c for c in (answers.get("chronic") or []) if c != "none"],
        "payment_context": payment_context,
        "funding_confidence": funding_conf,
        "audiencing_snapshot": dict(aud),
        "DecisionTrace": []
    }

    # DecisionTrace order: rec first
    gcp["DecisionTrace"].append({"rule_id": decision_id, "why": "Primary recommendation rule"})
    # Medicaid nudge second
    if payment_context == "medicaid":
        gcp["DecisionTrace"].append({"rule_id": "gcp.nudge.medicaid_path", "why": "Medicaid pathway"})
    # Funding confidence nudge third (private only)
    if payment_context == "private" and funding_conf in {"unsure","not_confident"}:
        gcp["DecisionTrace"].append({"rule_id": "gcp.nudge.financial_confidence", "why": f"Funding confidence is '{funding_conf}'"})

    # Analytics trace (primary)
    trace("gcp.recommended_setting", f"{gcp['recommended_setting']}/{gcp['care_intensity']} ({payment_context})", "gcp",
          rule_id=gcp["DecisionTrace"][0]["rule_id"], extra={"safety_flags": gcp["safety_flags"]})

    # Context for callers
    context = {
        "derived": {
            "cognition": cog, "adl": adl, "meds": meds, "falls": fall, "home": home, "mobility": mob,
            "supervision": sup, "isolation": iso, "access": acc, "caregiver_support": support, "behavior": behav_val
        },
        "route": route,
        "medicaid_unsure_flag": medicaid_unsure_flag
    }

    return context, gcp
