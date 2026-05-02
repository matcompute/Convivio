# Convivio

Convivio is an AI go-to-market suite for restaurants and hospitality teams that want coordinated campaign planning, review response support, retention playbooks, and brand-safe marketing output from one workspace.

The name comes from the Italian word `convivio`, which suggests gathering, dining together, and shared hospitality. It fits a product built for customer-facing hospitality growth.

## Product Position

Convivio is positioned as an AI growth platform for hospitality teams that need brand-safe commercial execution:

- strong Python + React full-stack story
- applied LLM and agent orchestration direction
- practical business use for restaurants and hospitality SMEs
- clear bridge between AI engineering and product engineering
- strong fit for AI Engineer, Applied AI, and agent-platform roles

## Stack

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- React 18
- Vite 5
- custom responsive CSS system

## Current Features

- demo-authenticated workspace for hospitality marketing teams
- restaurant profile and brand context editor
- AI campaign studio with strategist, copy, and retention outputs
- review desk for response drafting with tone guidance
- retention lab for loyalty and win-back playbooks
- dashboard metrics for campaign throughput, review pressure, and repeat-guest focus
- Gemini provider support with a safe mock fallback
- portable backend and frontend run scripts for local development

## How It Works

Convivio is designed around a simple hospitality operator workflow:

1. Sign in with a workspace account.
2. Define or refine the restaurant profile so the system has brand context.
3. Create a campaign brief and let the strategist flow generate channel-ready output.
4. Review guest feedback in the review desk and draft responses with tone control.
5. Generate a retention play when the team wants to recover repeat traffic or strengthen weekday demand.
6. Approve strong output and iterate on weaker output without leaving the workspace.

The current version uses seeded workspace data for a realistic walkthrough, but the campaign, review, and retention generation paths can be powered by Gemini through the backend provider layer.

## Demo Accounts

All seeded users share the same password:

```text
Convivio123!
```

Recommended logins:

- `owner@convivio.io`
- `marketing@convivio.io`
- `ops@convivio.io`

## Local Run

Environment:

```powershell
cd backend
Copy-Item .env.example .env
```

Then set:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

If you want local development without a live model call, use:

```env
LLM_PROVIDER=mock
```

Backend:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5061
```

Frontend:

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 4203
```

Open:

```text
http://127.0.0.1:4203
```

API health:

```text
http://127.0.0.1:5061/api/health
```

## Verification

Backend health:

```powershell
Invoke-RestMethod http://127.0.0.1:5061/api/health
```

Frontend production build:

```powershell
cd frontend
npm run build
```

Gemini-backed smoke test:

```powershell
cd backend
.\.venv\Scripts\python.exe -c "from app.api.schemas import CampaignBriefRequest; from app.services.agent_service import build_campaign_output; from app.store.demo_store import get_profile; brief = CampaignBriefRequest(title='Weekday revival', objective='Increase weekday bookings', audience='Local repeat guests', channel_mix=['Instagram'], offer='Chef pairing', timing='This week', notes='Keep it elegant.'); print(build_campaign_output(brief, get_profile())['strategist_summary'])"
```

## Engineering Focus

Convivio is structured to demonstrate:

- Python backend delivery for AI workflows
- agent-oriented orchestration patterns
- LLM-ready product design
- prompt/output approval workflow design
- frontend delivery for a polished AI workspace
- business-facing AI workflow design instead of notebook-only experimentation

## Roadmap

- provider abstraction for OpenAI, Anthropic, and local open-source models
- retrieval from menus, reviews, and brand documents
- campaign approval history and publishing connectors
- evaluation dashboard for output quality, cost, and latency
- multi-tenant workspace and billing readiness
