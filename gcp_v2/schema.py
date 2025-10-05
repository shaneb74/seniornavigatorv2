from __future__ import annotations

# Sections (render order)
SECTIONS = [
    ("financial", "Financial"),
    ("daily_life_support", "Daily Life & Support"),
    ("health_safety", "Health & Safety"),
    ("context_prefs", "Context & Preferences"),
]

# Questions, stable IDs + mappings
QUESTIONS = [
    # Financial
    {
        "id": "medicaid_status",
        "section": "financial",
        "order": 0,
        "label": "Are you currently enrolled in Medicaid or receiving state long-term care assistance?",
        "type": "single",
        "choices": [
            ("yes", "Yes"),
            ("no", "No"),
            ("unsure", "Unsure"),
        ],
        "helper": 'Medicare is federal health insurance. Medicaid is a need-based program that can pay for long-term care. If you’re unsure, keep going—we’ll flag this to double-check later.',
        "maps_to": "answers.medicaid_status",
        "notes": "If yes → medicaid off-ramp",
    },
    {
        "id": "funding_confidence",
        "section": "financial",
        "order": 1,
        "label": "How confident do you feel about paying for care?",
        "type": "single",
        "choices": [
            ("no_worries", "No worries"),
            ("confident", "Confident"),
            ("unsure", "Unsure"),
            ("not_confident", "Not confident"),
        ],
        "visible_if": {"medicaid_status__ne": "yes"},
        "maps_to": "answers.funding_confidence",
    },

    # Daily Life & Support
    {"id": "who_for", "section": "daily_life_support", "order": 2,
     "label": "Who are you planning for?", "type": "single",
     "choices": [("self","Myself"),("parent","Parent"),("spouse","Spouse/Partner"),("other","Other")],
     "maps_to": "answers.who_for"},
    {"id": "living_now", "section": "daily_life_support", "order": 3,
     "label": "Where do they live today?", "type": "single",
     "choices": [("own_home","Own home"),("with_family","With family"),("independent","Independent Living"),
                 ("assisted","Assisted Living"),("memory","Memory Care"),("skilled","Skilled Nursing")],
     "maps_to": "answers.living_now"},
    {"id": "caregiver_support", "section": "daily_life_support", "order": 4,
     "label": "How much caregiver support is available?", "type": "single",
     "choices": [("none","None"),("few_days_week","A few days/week"),("most_days","Most days"),("24_7","24/7")],
     "maps_to": "answers.caregiver_support"},
    {"id": "adl_help", "section": "daily_life_support", "order": 5,
     "label": "How many daily activities need help?", "type": "single",
     "choices": [("0-1","0–1"),("2-3","2–3"),("4-5","4–5"),("6+","6+")],
     "maps_to": "answers.adl_help"},

    # Health & Safety
    {"id": "cognition", "section": "health_safety", "order": 6,
     "label": "How is memory and thinking?", "type": "single",
     "choices": [("normal","Normal"),("mild","Mild changes"),("moderate","Moderate"),("severe","Severe")],
     "maps_to": "answers.cognition"},
    {"id": "behavior_risks", "section": "health_safety", "order": 7,
     "label": "Any wandering or unsafe behaviors?", "type": "multi",
     "choices": [("wandering","Wandering"),("agitation","Agitation"),("exit_seeking","Exit seeking"),("none","None")],
     "maps_to": "answers.behavior_risks"},
    {"id": "falls", "section": "health_safety", "order": 8,
     "label": "Falls in the last 12 months?", "type": "single",
     "choices": [("none","None"),("one","One"),("recurrent","Recurrent")],
     "maps_to": "answers.falls"},
    {"id": "med_mgmt", "section": "health_safety", "order": 9,
     "label": "How complex are medications to manage?", "type": "single",
     "choices": [("simple","Simple"),("several","Several meds"),("complex","Complex regimen")],
     "maps_to": "answers.med_mgmt"},
    {"id": "home_safety", "section": "health_safety", "order": 10,
     "label": "Is the home setup safe (stairs/bath/etc.)?",
     "type": "single",
     "choices": [("safe","Safe"),("some_risks","Some risks"),("unsafe","Unsafe")],
     "maps_to": "answers.home_safety"},
    {"id": "supervision", "section": "health_safety", "order": 11,
     "label": "Do they have needed supervision at home?",
     "type": "single",
     "choices": [("always","Always"),("sometimes","Sometimes"),("rarely","Rarely"),("never","Never")],
     "maps_to": "answers.supervision"},

    # Context & Preferences
    {"id": "chronic", "section": "context_prefs", "order": 12,
     "label": "Any chronic conditions?", "type": "multi",
     "choices": [("diabetes","Diabetes"),("parkinson","Parkinson’s"),("stroke","Stroke"),
                 ("copd","COPD"),("chf","CHF"),("other","Other"),("none","None")],
     "maps_to": "answers.chronic"},
    {"id": "preferences", "section": "context_prefs", "order": 13,
     "label": "Any strong preferences?", "type": "multi",
     "choices": [("stay_home","Stay at home"),("be_near_family","Be near family"),
                 ("structured_care","Structured care"),("private_room","Private room"),("none","None")],
     "maps_to": "answers.preferences"},
]

# Simple helpers
def questions_for_section(section: str):
    return sorted([q for q in QUESTIONS if q["section"] == section], key=lambda x: x["order"])
