# Trivia bank for Waiting Room daily questions
from __future__ import annotations

from typing import Any, Dict, List, Optional

QUESTIONS: List[Dict[str, Any]] = [
    {
        "question": "What is one of the biggest advantages of independent living communities?",
        "options": [
            "On-site emergency medical staff 24/7",
            "Maintenance-free housing with social activities",
            "Intensive nursing care delivered in-room",
            "Hospital-level rehabilitation services",
        ],
        "correct_index": 1,
        "explanation": "Independent living communities focus on maintenance-free residences plus dining, transportation, and social programming—great for active seniors who want ease and connection.",
        "topic": "Housing",
    },
    {
        "question": "Which home modification most reduces fall risk around entryways?",
        "options": [
            "Installing exterior railings and slip-resistant steps",
            "Adding smart speakers in common rooms",
            "Replacing all interior doors with sliding doors",
            "Painting door frames contrasting colors",
        ],
        "correct_index": 0,
        "explanation": "Secure railings, slip-resistant materials, and proper lighting at entrances address one of the highest-risk fall zones around the home.",
        "topic": "Safety",
    },
    {
        "question": "Medicare covers which part of long-term custodial care?",
        "options": [
            "Ongoing assistance with bathing and dressing at home",
            "Unlimited nursing home stays past 100 days",
            "Short-term skilled nursing after a qualifying hospital stay",
            "Room and board in assisted living communities",
        ],
        "correct_index": 2,
        "explanation": "Traditional Medicare pays for skilled nursing or rehab after a hospital stay (usually up to 100 days) but not long-term custodial or assisted living costs.",
        "topic": "Benefits",
    },
    {
        "question": "What’s a common sign it may be time to reassess caregiving support?",
        "options": [
            "Care partner requests more shared calendars",
            "Frequent missed medications or appointment confusion",
            "Family schedules a weekly phone check-in",
            "Loved one joins a community choir",
        ],
        "correct_index": 1,
        "explanation": "Medication errors or missed appointments often signal burnout or rising care complexity—an early cue to add professional support or respite.",
        "topic": "Caregiving",
    },
    {
        "question": "Which document names someone to make decisions if you can’t?",
        "options": [
            "Advance directive / durable power of attorney",
            "Standard lease agreement",
            "Medigap insurance rider",
            "Living will for funeral arrangements",
        ],
        "correct_index": 0,
        "explanation": "A durable power of attorney (often part of an advance directive) authorizes someone to manage health or financial decisions if you become unable.",
        "topic": "Legal & Planning",
    },
    {
        "question": "VA Aid & Attendance benefits can help pay for what?",
        "options": [
            "Home safety renovations only",
            "Home care, assisted living, or nursing care for qualifying veterans",
            "College tuition for grandchildren",
            "Mortgage refinancing assistance",
        ],
        "correct_index": 1,
        "explanation": "Aid & Attendance provides a monthly benefit to qualifying veterans or surviving spouses who need help with daily activities, usable for home or facility care.",
        "topic": "Benefits",
    },
    {
        "question": "What is one benefit of creating a care timeline?",
        "options": [
            "Locks in provider prices for five years",
            "Identifies upcoming transitions so you can budget and staff ahead",
            "Eliminates the need for legal planning documents",
            "Automatically qualifies for Medicaid",
        ],
        "correct_index": 1,
        "explanation": "Mapping likely transitions—like selling a home or needing more help—lets families line up resources, team members, and budget adjustments before a crisis hits.",
        "topic": "Planning",
    },
    {
        "question": "Which funding source is typically best for near-term care expenses?",
        "options": [
            "Illiquid real estate equity",
            "Long-term annuities with surrender penalties",
            "Liquid savings and low-volatility accounts",
            "Selling collectibles and art at auction",
        ],
        "correct_index": 2,
        "explanation": "Liquid savings offer predictable access without penalty or market timing risk, making them the most reliable plug for near-term care gaps.",
        "topic": "Finances",
    },
    {
        "question": "Routine medication reviews are recommended how often?",
        "options": [
            "Every 3–5 years unless symptoms change",
            "Only after a hospital stay",
            "At least annually or when new symptoms appear",
            "Once at age 65 then never again",
        ],
        "correct_index": 2,
        "explanation": "Annual medication reviews—or sooner if health changes—catch interactions, duplications, and opportunities to simplify complex regimens.",
        "topic": "Health",
    },
    {
        "question": "What’s a quick win for reducing nighttime wandering risks?",
        "options": [
            "Removing all interior nightlights",
            "Adding motion-activated lighting and door alarms",
            "Locking the refrigerator overnight",
            "Scheduling daytime naps every hour",
        ],
        "correct_index": 1,
        "explanation": "Motion-activated path lighting and discreet door alarms gently deter unsafe wandering and alert caregivers without being overly restrictive.",
        "topic": "Safety",
    },
    {
        "question": "Which professional can help evaluate driving safety for older adults?",
        "options": [
            "Certified driving rehabilitation specialist",
            "Financial advisor",
            "Primary school teacher",
            "Mortgage broker",
        ],
        "correct_index": 0,
        "explanation": "Certified driving rehabilitation specialists or occupational therapists trained in driving assessments can provide impartial, safety-focused evaluations.",
        "topic": "Mobility",
    },
]


def get_daily_question(datekey: str) -> Optional[Dict[str, Any]]:
    """
    Return a deterministic question for the provided date key.
    If the bank is empty, return None.
    """
    if not QUESTIONS:
        return None
    safe_key = (datekey or "").strip()
    if not safe_key:
        safe_key = "default"
    seed = sum(ord(ch) for ch in safe_key)
    return QUESTIONS[seed % len(QUESTIONS)]
