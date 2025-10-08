from guided_care_plan.engine import evaluate_guided_care

def _base(over=None):
    a = {
        "medicaid_status":"no","funding_confidence":"unsure",
        "adl_help":"2-3","caregiver_support":"most_days",
        "cognition":"mild","behavior_risks":[],
        "falls":"none","med_mgmt":"several","mobility":"no_issues","supervision":"always","home_safety":"safe",
        "social_isolation":"weekly","geographic_access":"moderate","chronic":[]
    }
    if over: a.update(over)
    return a

def test_medicaid_precedence_yes():
    ctx, g = evaluate_guided_care(_base({"medicaid_status":"yes"}), {"on_medicaid": False})
    assert g["payment_context"] == "medicaid"
    assert ctx.get("route") == "medicaid_offramp"
    assert any(t["rule_id"]=="gcp.nudge.medicaid_path" for t in g["DecisionTrace"])

def test_medicaid_precedence_aud():
    ctx, g = evaluate_guided_care(_base({"medicaid_status":"no"}), {"on_medicaid": True})
    assert g["payment_context"] == "medicaid"

def test_unsure_sets_flag_and_financial_nudge():
    ctx, g = evaluate_guided_care(_base({"medicaid_status":"unsure","funding_confidence":"not_confident"}), {})
    assert ctx.get("medicaid_unsure_flag") is True
    assert g["payment_context"] == "private"
    assert any(t["rule_id"]=="gcp.nudge.financial_confidence" for t in g["DecisionTrace"])
