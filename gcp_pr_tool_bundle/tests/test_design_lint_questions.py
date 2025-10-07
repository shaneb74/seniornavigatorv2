import csv, os

def test_design_lint_questions():
    path = os.path.join(os.path.dirname(__file__), "..", "guided_care_plan", "questions", "questions.csv")
    rows = list(csv.DictReader(open(path, "r", encoding="utf-8")))
    ids = {r["id"] for r in rows}
    expected = {"medicaid_status","funding_confidence","adl_help","caregiver_support","cognition","behavior_risks","falls","med_mgmt","mobility","supervision","home_safety","social_isolation","geographic_access","chronic"}
    assert expected.issubset(ids)
    # funding choices
    fc = {r["choice_id"] for r in rows if r["id"]=="funding_confidence"}
    assert fc == {"no_worries","confident","unsure","not_confident"}
    mc = {r["choice_id"] for r in rows if r["id"]=="medicaid_status"}
    assert mc == {"yes","no","unsure"}
