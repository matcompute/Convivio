from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.schemas import (
    CampaignApprovalResponse,
    CampaignBriefRequest,
    CampaignRecordDto,
    DashboardResponse,
    HealthResponse,
    LoginRequest,
    LoginResponse,
    RestaurantProfileDto,
    RetentionPlanDto,
    RetentionRequest,
    ReviewResponseRequest,
    ReviewResponseResult,
    ReviewTicketDto,
    UserDto,
)
from app.core.settings import settings
from app.services.agent_service import build_campaign_output, build_retention_plan, build_review_response
from app.store import demo_store


router = APIRouter(prefix=settings.api_prefix)
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")

    user = demo_store.get_user_by_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is invalid.")

    return user


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="convivio-api")


@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    user = demo_store.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    token = demo_store.create_session(user["id"])
    return LoginResponse(access_token=token, user=UserDto(**user))


@router.get("/auth/me", response_model=UserDto)
def me(user: dict = Depends(get_current_user)) -> UserDto:
    return UserDto(**user)


@router.get("/business/profile", response_model=RestaurantProfileDto)
def get_profile(user: dict = Depends(get_current_user)) -> RestaurantProfileDto:
    return RestaurantProfileDto(**demo_store.get_profile())


@router.put("/business/profile", response_model=RestaurantProfileDto)
def update_profile(payload: RestaurantProfileDto, user: dict = Depends(get_current_user)) -> RestaurantProfileDto:
    profile = demo_store.update_profile(payload.model_dump())
    return RestaurantProfileDto(**profile)


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(user: dict = Depends(get_current_user)) -> DashboardResponse:
    campaigns = demo_store.list_campaigns()
    reviews = demo_store.list_reviews()
    plans = demo_store.list_retention_plans()
    profile = demo_store.get_profile()

    metrics = [
        {
            "label": "Campaigns Ready",
            "value": str(len(campaigns)),
            "detail": "Approved and draft go-to-market plays",
            "trend": "+2 this week",
        },
        {
            "label": "Reviews Waiting",
            "value": str(len([item for item in reviews if item["status"] != "Closed"])),
            "detail": "Guest reviews needing response or recovery",
            "trend": "1 at-risk review",
        },
        {
            "label": "Retention Plays",
            "value": str(len(plans)),
            "detail": "Active loyalty or win-back plans",
            "trend": "Weekday recovery focus",
        },
        {
            "label": "Primary Goal",
            "value": profile["current_goal"],
            "detail": "Current commercial objective",
            "trend": "Operator-defined",
        },
    ]
    highlights = [
        {
            "id": "evt-1",
            "title": "Thursday campaign approved",
            "detail": "Aperitivo-focused campaign is ready to publish across Instagram and email.",
            "timestamp": campaigns[0]["created_at"],
            "tone": "positive",
        },
        {
            "id": "evt-2",
            "title": "Guest recovery needed",
            "detail": "One Google review highlights slow pacing and needs a careful response.",
            "timestamp": campaigns[0]["created_at"],
            "tone": "attention",
        },
    ]
    return DashboardResponse(
        metrics=metrics,
        active_objectives=[
            "Protect premium brand tone",
            "Increase weekday repeat bookings",
            "Recover at-risk guest feedback quickly",
        ],
        highlights=highlights,
    )


@router.get("/campaigns", response_model=list[CampaignRecordDto])
def list_campaigns(user: dict = Depends(get_current_user)) -> list[CampaignRecordDto]:
    return [CampaignRecordDto(**item) for item in demo_store.list_campaigns()]


@router.post("/campaigns/generate", response_model=CampaignRecordDto)
def generate_campaign(payload: CampaignBriefRequest, user: dict = Depends(get_current_user)) -> CampaignRecordDto:
    profile = demo_store.get_profile()
    record = build_campaign_output(payload, profile)
    saved = demo_store.add_campaign(record)
    return CampaignRecordDto(**saved)


@router.post("/campaigns/{campaign_id}/approve", response_model=CampaignApprovalResponse)
def approve_campaign(campaign_id: str, user: dict = Depends(get_current_user)) -> CampaignApprovalResponse:
    campaign = demo_store.approve_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found.")
    return CampaignApprovalResponse(
        campaign=CampaignRecordDto(**campaign),
        message="Campaign approved and ready for downstream publishing.",
    )


@router.get("/reviews", response_model=list[ReviewTicketDto])
def list_reviews(user: dict = Depends(get_current_user)) -> list[ReviewTicketDto]:
    return [ReviewTicketDto(**item) for item in demo_store.list_reviews()]


@router.post("/reviews/respond", response_model=ReviewResponseResult)
def draft_review_response(payload: ReviewResponseRequest, user: dict = Depends(get_current_user)) -> ReviewResponseResult:
    profile = demo_store.get_profile()
    reviews = demo_store.list_reviews()
    review = next((item for item in reviews if item["id"] == payload.review_id), None)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")

    drafted_response, coaching_note = build_review_response(review, payload, profile)
    updated = demo_store.update_review(payload.review_id, drafted_response)
    return ReviewResponseResult(review=ReviewTicketDto(**updated), coaching_note=coaching_note)


@router.get("/retention/plans", response_model=list[RetentionPlanDto])
def list_retention_plans(user: dict = Depends(get_current_user)) -> list[RetentionPlanDto]:
    return [RetentionPlanDto(**item) for item in demo_store.list_retention_plans()]


@router.post("/retention/generate", response_model=RetentionPlanDto)
def generate_retention_plan(payload: RetentionRequest, user: dict = Depends(get_current_user)) -> RetentionPlanDto:
    profile = demo_store.get_profile()
    record = build_retention_plan(payload, profile)
    saved = demo_store.add_retention_plan(record)
    return RetentionPlanDto(**saved)

