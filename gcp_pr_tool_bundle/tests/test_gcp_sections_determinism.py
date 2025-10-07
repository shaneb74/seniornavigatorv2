from guided_care_plan.engine import evaluate_guided_care

def answersA():
    return {
        "medicaid_status":"yes","funding_confidence":"unsure",
        "adl_help":"2-3","caregiver_support":"most_days",
        "cognition":"mild","behavior_risks":[],
        "falls":"none","med_mgmt":"several","mobility":"no_issues","supervision":"always","home_safety":"safe",
        "social_isolation":"weekly","geographic_access":"moderate","chronic":[]
    }

def answersB():
    return {
        "medicaid_status":"no","funding_confidence":"unsure",
        "adl_help":"2-3","caregiver_support":"most_days",
        "cognition":"mild","behavior_risks":[],
        "falls":"none","med_mgmt":"several","mobility":"no_issues","supervision":"always","home_safety":"safe",
        "social_isolation":"weekly","geographic_access":"moderate","chronic":[]
    }

def test_determinism_path_yes():
    aud = {"on_medicaid": False}
    ctx1, g1 = evaluate_guided_care(answersA(), aud)
    ctx2, g2 = evaluate_guided_care(answersA(), aud)
    assert g1 == g2
    assert ctx1["derived"] == ctx2["derived"]

def test_determinism_path_not_yes():
    aud = {"on_medicaid": False}
    ctx1, g1 = evaluate_guided_care(answersB(), aud)
    ctx2, g2 = evaluate_guided_care(answersB(), aud)
    assert g1 == g2
