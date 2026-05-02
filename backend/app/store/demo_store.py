from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from uuid import uuid4


UTC = timezone.utc

USERS = [
    {
        "id": "usr-owner",
        "full_name": "Giulia Conti",
        "email": "owner@convivio.io",
        "password": "Convivio123!",
        "role": "Owner",
    },
    {
        "id": "usr-marketing",
        "full_name": "Marco Bellini",
        "email": "marketing@convivio.io",
        "password": "Convivio123!",
        "role": "Marketing Lead",
    },
    {
        "id": "usr-ops",
        "full_name": "Sara Ferri",
        "email": "ops@convivio.io",
        "password": "Convivio123!",
        "role": "Operations Manager",
    },
]

SESSIONS: dict[str, str] = {}

RESTAURANT_PROFILE = {
    "name": "Lume Bistro",
    "city": "Florence",
    "cuisine": "Modern Tuscan",
    "concept": "Intimate neighborhood dining with seasonal tasting menus and aperitivo moments.",
    "target_audience": "Young professionals, local couples, and city-break travelers seeking premium casual dining.",
    "voice": "Warm, polished, and confident with a welcoming local tone.",
    "hero_offer": "Thursday aperitivo pairing with chef small plates.",
    "current_goal": "Increase repeat reservations on weekdays without discounting the core dinner experience.",
    "channels": [
        {"channel": "Instagram", "handle": "@lumebistrofi", "focus": "Visual storytelling and event hooks"},
        {"channel": "Email", "handle": "club@lumebistro.it", "focus": "VIP offers and repeat-guest nudges"},
        {"channel": "WhatsApp", "handle": "+39 055 555 0184", "focus": "Short lead-time booking pushes"},
    ],
}

CAMPAIGNS = [
    {
        "id": "cmp-1101",
        "title": "Weeknight Aperitivo Lift",
        "objective": "Lift Thursday covers",
        "audience": "Local professionals within 5km",
        "status": "Approved",
        "created_at": datetime.now(UTC) - timedelta(days=2, hours=3),
        "strategist_summary": "Pair a low-friction aperitivo hook with a chef-driven scarcity message to make Thursday feel like a limited weekly ritual.",
        "suggested_offer": "Reserve by Wednesday for a welcome citrus spritz pairing.",
        "channel_drafts": [
            {
                "channel": "Instagram",
                "headline": "Thursday deserves a ritual",
                "body": "Chef pairings, candlelight, and a welcome spritz for early bookings.",
                "cta": "Book your Thursday table",
            },
            {
                "channel": "Email",
                "headline": "A quieter Florence, a better table",
                "body": "This Thursday, we are turning aperitivo into a guided tasting moment for regulars and friends.",
                "cta": "Reserve now",
            },
        ],
    }
]

REVIEWS = [
    {
        "id": "rev-701",
        "guest_name": "Alessia R.",
        "source": "Google",
        "rating": 3,
        "sentiment": "At risk",
        "issue": "Slow main course pacing",
        "review_text": "Food was lovely, but we waited too long between courses and almost left before dessert.",
        "status": "Needs response",
        "drafted_response": None,
    },
    {
        "id": "rev-702",
        "guest_name": "Thomas P.",
        "source": "Tripadvisor",
        "rating": 5,
        "sentiment": "Positive",
        "issue": "Excellent staff warmth",
        "review_text": "The team made us feel instantly at home. The wine recommendation was perfect.",
        "status": "Needs response",
        "drafted_response": None,
    },
]

RETENTION_PLANS = [
    {
        "id": "ret-4001",
        "objective": "Recover lapsed weekday guests",
        "segment": "Guests absent for 45+ days after two prior visits",
        "summary": "Use a low-pressure return invitation tied to new seasonal pairings and social proof from recent reviews.",
        "actions": [
            {
                "step": "Segment refresh",
                "trigger": "Every Monday morning",
                "action": "Identify weekday guests inactive for 45 days with prior spend above the median.",
            },
            {
                "step": "Invite",
                "trigger": "Within 2 hours of segment refresh",
                "action": "Send a warm note with a seasonal chef pairing invitation and booking link.",
            },
        ],
        "created_at": datetime.now(UTC) - timedelta(days=4),
    }
]


def _safe_user(user: dict) -> dict:
    return {key: value for key, value in user.items() if key != "password"}


def authenticate(email: str, password: str) -> dict | None:
    for user in USERS:
        if user["email"].lower() == email.lower() and user["password"] == password:
            return _safe_user(user)
    return None


def create_session(user_id: str) -> str:
    token = f"convivio-{uuid4().hex}"
    SESSIONS[token] = user_id
    return token


def get_user_by_token(token: str) -> dict | None:
    user_id = SESSIONS.get(token)
    if not user_id:
        return None
    for user in USERS:
        if user["id"] == user_id:
            return _safe_user(user)
    return None


def get_profile() -> dict:
    return deepcopy(RESTAURANT_PROFILE)


def update_profile(payload: dict) -> dict:
    RESTAURANT_PROFILE.update(deepcopy(payload))
    return get_profile()


def list_campaigns() -> list[dict]:
    return deepcopy(sorted(CAMPAIGNS, key=lambda item: item["created_at"], reverse=True))


def add_campaign(record: dict) -> dict:
    CAMPAIGNS.append(record)
    return deepcopy(record)


def approve_campaign(campaign_id: str) -> dict | None:
    for campaign in CAMPAIGNS:
        if campaign["id"] == campaign_id:
            campaign["status"] = "Approved"
            return deepcopy(campaign)
    return None


def list_reviews() -> list[dict]:
    return deepcopy(REVIEWS)


def update_review(review_id: str, drafted_response: str) -> dict | None:
    for review in REVIEWS:
        if review["id"] == review_id:
            review["drafted_response"] = drafted_response
            review["status"] = "Draft ready"
            return deepcopy(review)
    return None


def list_retention_plans() -> list[dict]:
    return deepcopy(sorted(RETENTION_PLANS, key=lambda item: item["created_at"], reverse=True))


def add_retention_plan(record: dict) -> dict:
    RETENTION_PLANS.append(record)
    return deepcopy(record)

