from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserDto(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserDto


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str


class BrandChannelDto(BaseModel):
    channel: str
    handle: str
    focus: str


class RestaurantProfileDto(BaseModel):
    name: str
    city: str
    cuisine: str
    concept: str
    target_audience: str
    voice: str
    hero_offer: str
    current_goal: str
    channels: list[BrandChannelDto]


class DashboardMetricDto(BaseModel):
    label: str
    value: str
    detail: str
    trend: str


class TimelineItemDto(BaseModel):
    id: str
    title: str
    detail: str
    timestamp: datetime
    tone: str


class DashboardResponse(BaseModel):
    metrics: list[DashboardMetricDto]
    active_objectives: list[str]
    highlights: list[TimelineItemDto]


class CampaignBriefRequest(BaseModel):
    title: str = Field(min_length=4, max_length=120)
    objective: str = Field(min_length=4, max_length=120)
    audience: str = Field(min_length=4, max_length=120)
    channel_mix: list[str] = Field(min_length=1)
    offer: str = Field(min_length=4, max_length=200)
    timing: str = Field(min_length=4, max_length=120)
    notes: str = Field(default="", max_length=600)


class ChannelDraftDto(BaseModel):
    channel: str
    headline: str
    body: str
    cta: str


class CampaignRecordDto(BaseModel):
    id: str
    title: str
    objective: str
    audience: str
    status: str
    created_at: datetime
    strategist_summary: str
    suggested_offer: str
    channel_drafts: list[ChannelDraftDto]


class CampaignApprovalResponse(BaseModel):
    campaign: CampaignRecordDto
    message: str


class ReviewTicketDto(BaseModel):
    id: str
    guest_name: str
    source: str
    rating: int
    sentiment: str
    issue: str
    review_text: str
    status: str
    drafted_response: str | None = None


class ReviewResponseRequest(BaseModel):
    review_id: str
    tone: Literal["warm", "apologetic", "confident", "celebratory"]
    recovery_offer: str = Field(default="", max_length=200)


class ReviewResponseResult(BaseModel):
    review: ReviewTicketDto
    coaching_note: str


class RetentionRequest(BaseModel):
    objective: str = Field(min_length=4, max_length=120)
    at_risk_segment: str = Field(min_length=4, max_length=120)
    incentive: str = Field(min_length=4, max_length=120)
    horizon_days: int = Field(ge=7, le=180)


class RetentionPlayDto(BaseModel):
    step: str
    trigger: str
    action: str


class RetentionPlanDto(BaseModel):
    id: str
    objective: str
    segment: str
    summary: str
    actions: list[RetentionPlayDto]
    created_at: datetime

