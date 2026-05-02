from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any
from urllib import error, request
from uuid import uuid4

from app.api.schemas import CampaignBriefRequest, RetentionRequest, ReviewResponseRequest
from app.core.settings import settings


logger = logging.getLogger(__name__)


def _mock_campaign_output(brief: CampaignBriefRequest, profile: dict) -> dict:
    focus_line = (
        f"Position {profile['name']} as the easiest premium choice for {brief.audience.lower()} "
        f"while making {brief.offer.lower()} feel time-sensitive but still brand-safe."
    )
    channel_drafts = []

    for channel in brief.channel_mix:
        channel_drafts.append(
            {
                "channel": channel,
                "headline": f"{brief.title} | {profile['city']} edition",
                "body": (
                    f"{profile['name']} is spotlighting {brief.offer.lower()} for {brief.timing.lower()}. "
                    f"Keep the tone {profile['voice'].lower()} and frame the moment around {brief.objective.lower()}."
                ),
                "cta": f"Reserve now for {brief.timing.lower()}",
            }
        )

    return {
        "strategist_summary": focus_line,
        "suggested_offer": brief.offer,
        "channel_drafts": channel_drafts,
    }


def _mock_review_response(review: dict, review_request: ReviewResponseRequest, profile: dict) -> tuple[str, str]:
    tone_openers = {
        "warm": "Thank you for sharing this with us",
        "apologetic": "We are genuinely sorry this part of your visit felt off",
        "confident": "Thank you for the clear feedback",
        "celebratory": "We loved reading this",
    }

    drafted = (
        f"{tone_openers[review_request.tone]}, {review['guest_name']}. "
        f"At {profile['name']}, we want every guest experience to feel {profile['voice'].lower()}. "
        f"We appreciate your note about {review['issue'].lower()}. "
        f"{review_request.recovery_offer + '. ' if review_request.recovery_offer else ''}"
        f"If you visit again, we would love the chance to make the next experience even better."
    )

    coaching = (
        "Acknowledge the issue early, keep the response human, and use the recovery offer only as a supportive gesture."
    )
    return drafted, coaching


def _mock_retention_plan(retention_request: RetentionRequest, profile: dict) -> dict:
    return {
        "summary": (
            f"Use {retention_request.incentive.lower()} as a light re-entry trigger for guests in the "
            f"{retention_request.at_risk_segment.lower()} segment, while keeping the brand tone "
            f"{profile['voice'].lower()} over a {retention_request.horizon_days}-day window."
        ),
        "actions": [
            {
                "step": "Audience refresh",
                "trigger": "Every Monday",
                "action": f"Identify guests matching {retention_request.at_risk_segment.lower()} and score them for return likelihood.",
            },
            {
                "step": "Warm invite",
                "trigger": "Within 4 hours of audience refresh",
                "action": f"Send a personalized note centered on {retention_request.incentive.lower()} and the current brand goal.",
            },
            {
                "step": "Follow-up",
                "trigger": f"Day {min(10, retention_request.horizon_days // 3)} if unopened",
                "action": "Switch to a shorter reminder with a simpler booking CTA and social proof snippet.",
            },
        ],
    }


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    return json.loads(cleaned)


def _gemini_generate_json(prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": response_schema,
        },
    }

    endpoint = f"{settings.gemini_api_base}/models/{settings.gemini_model}:generateContent"
    request_body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        endpoint,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": settings.gemini_api_key,
        },
        method="POST",
    )

    with request.urlopen(http_request, timeout=settings.llm_timeout_seconds) as response:
        raw = json.loads(response.read().decode("utf-8"))

    try:
        text = raw["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Gemini returned an unexpected response shape.") from exc

    return _extract_json(text)


def _build_campaign_prompt(brief: CampaignBriefRequest, profile: dict) -> str:
    return f"""
You are the strategist and campaign copy system for a hospitality growth platform.

Restaurant profile:
- Name: {profile['name']}
- City: {profile['city']}
- Cuisine: {profile['cuisine']}
- Concept: {profile['concept']}
- Audience: {profile['target_audience']}
- Brand voice: {profile['voice']}
- Current goal: {profile['current_goal']}
- Hero offer: {profile['hero_offer']}

Campaign brief:
- Title: {brief.title}
- Objective: {brief.objective}
- Audience: {brief.audience}
- Offer: {brief.offer}
- Timing: {brief.timing}
- Notes: {brief.notes}
- Channels: {", ".join(brief.channel_mix)}

Return marketing output that sounds premium, warm, and commercially sharp for a restaurant team.
Keep each channel draft concise, practical, and ready for a human approver.
""".strip()


def _build_review_prompt(review: dict, review_request: ReviewResponseRequest, profile: dict) -> str:
    return f"""
You are drafting a review response for a hospitality brand.

Restaurant profile:
- Name: {profile['name']}
- Voice: {profile['voice']}
- Concept: {profile['concept']}

Review details:
- Guest: {review['guest_name']}
- Source: {review['source']}
- Rating: {review['rating']}
- Sentiment: {review['sentiment']}
- Issue: {review['issue']}
- Review text: {review['review_text']}

Response requirements:
- Tone: {review_request.tone}
- Recovery offer: {review_request.recovery_offer or 'None'}

Write a natural, brand-safe response that feels human, accountable, and concise.
Also include one short coaching note for the operator.
""".strip()


def _build_retention_prompt(retention_request: RetentionRequest, profile: dict) -> str:
    return f"""
You are a retention planning agent for a hospitality marketing platform.

Restaurant profile:
- Name: {profile['name']}
- City: {profile['city']}
- Cuisine: {profile['cuisine']}
- Brand voice: {profile['voice']}
- Current goal: {profile['current_goal']}

Retention brief:
- Objective: {retention_request.objective}
- At-risk segment: {retention_request.at_risk_segment}
- Incentive: {retention_request.incentive}
- Horizon days: {retention_request.horizon_days}

Create a practical retention plan with clear operator actions, simple timing, and a premium hospitality tone.
""".strip()


def _campaign_schema(channel_mix: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "strategist_summary": {"type": "string"},
            "suggested_offer": {"type": "string"},
            "channel_drafts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "enum": channel_mix},
                        "headline": {"type": "string"},
                        "body": {"type": "string"},
                        "cta": {"type": "string"},
                    },
                    "required": ["channel", "headline", "body", "cta"],
                },
            },
        },
        "required": ["strategist_summary", "suggested_offer", "channel_drafts"],
    }


def _review_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "drafted_response": {"type": "string"},
            "coaching_note": {"type": "string"},
        },
        "required": ["drafted_response", "coaching_note"],
    }


def _retention_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "actions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "step": {"type": "string"},
                        "trigger": {"type": "string"},
                        "action": {"type": "string"},
                    },
                    "required": ["step", "trigger", "action"],
                },
            },
        },
        "required": ["summary", "actions"],
    }


def _should_use_gemini() -> bool:
    return settings.llm_provider == "gemini" and bool(settings.gemini_api_key)


def build_campaign_output(brief: CampaignBriefRequest, profile: dict) -> dict:
    generated = None

    if _should_use_gemini():
        try:
            generated = _gemini_generate_json(
                _build_campaign_prompt(brief, profile),
                _campaign_schema(brief.channel_mix),
            )
        except (RuntimeError, error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            logger.warning("Gemini campaign generation failed; falling back to mock output: %s", exc)

    if not generated:
        generated = _mock_campaign_output(brief, profile)

    return {
        "id": f"cmp-{uuid4().hex[:8]}",
        "title": brief.title,
        "objective": brief.objective,
        "audience": brief.audience,
        "status": "Draft",
        "created_at": datetime.now(timezone.utc),
        "strategist_summary": generated["strategist_summary"],
        "suggested_offer": generated["suggested_offer"],
        "channel_drafts": generated["channel_drafts"],
    }


def build_review_response(review: dict, review_request: ReviewResponseRequest, profile: dict) -> tuple[str, str]:
    generated = None

    if _should_use_gemini():
        try:
            generated = _gemini_generate_json(
                _build_review_prompt(review, review_request, profile),
                _review_schema(),
            )
        except (RuntimeError, error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            logger.warning("Gemini review drafting failed; falling back to mock output: %s", exc)

    if not generated:
        return _mock_review_response(review, review_request, profile)

    return generated["drafted_response"], generated["coaching_note"]


def build_retention_plan(retention_request: RetentionRequest, profile: dict) -> dict:
    generated = None

    if _should_use_gemini():
        try:
            generated = _gemini_generate_json(
                _build_retention_prompt(retention_request, profile),
                _retention_schema(),
            )
        except (RuntimeError, error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            logger.warning("Gemini retention planning failed; falling back to mock output: %s", exc)

    if not generated:
        generated = _mock_retention_plan(retention_request, profile)

    return {
        "id": f"ret-{uuid4().hex[:8]}",
        "objective": retention_request.objective,
        "segment": retention_request.at_risk_segment,
        "summary": generated["summary"],
        "actions": generated["actions"],
        "created_at": datetime.now(timezone.utc),
    }
