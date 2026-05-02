# Convivio Product Blueprint

## 1. One-Line Pitch

Convivio is an AI go-to-market suite for restaurants and hospitality businesses that helps operators launch campaigns, answer reviews, and improve retention using coordinated AI workflows.

## 2. Why This Product

This is the right first AI portfolio product because it gives:

- a direct bridge from full-stack engineering into applied AI engineering
- a real multi-agent product story
- business value that is easy to explain to recruiters and buyers
- strong relevance to restaurant, hospitality, and SMB growth workflows
- a credible path toward sellable AI software

## 3. Users

### Restaurant Owner

- defines growth goals
- reviews campaign suggestions
- approves final output

### Marketing Manager

- creates campaign briefs
- manages channel copy
- reviews brand tone and output quality

### Operations Manager

- monitors review pressure and service risks
- coordinates offers around demand and capacity

### Growth Consultant

- manages multiple brands
- compares campaign performance and audience fit

## 4. Core Agents

- strategist agent
- channel copy agent
- review response agent
- retention planner agent
- quality and guardrail evaluator

## 5. Main Entities

- User
- Workspace
- RestaurantProfile
- BrandGuideline
- CampaignBrief
- CampaignOutput
- ReviewTicket
- ReviewResponseDraft
- RetentionPlan
- AudienceSegment
- ApprovalDecision
- ProviderRun

## 6. Core Screens

- login
- dashboard
- restaurant profile
- campaign studio
- review desk
- retention lab
- output approval history
- provider and evaluation panel

## 7. Initial Product Scope

### Backend

- demo auth and workspace access
- restaurant profile management
- dashboard metrics
- campaign generation workflow
- review response drafting
- retention plan generation
- token-based API structure ready for model providers later

### Frontend

- responsive AI workspace
- dashboard metrics and activity surface
- campaign brief form and generated outputs
- review queue and response drafting
- retention plan generation and display
- brand profile editing

## 8. Design Direction

Convivio should feel premium, warm, and energetic.

### Visual language

- deep midnight background
- pearl and soft sand text balance
- coral and tangerine for hospitality warmth
- teal and cyan for AI/system signals
- gold accents for conversion and premium moments

### UI tone

- product-grade, not toy chatbot
- spacious but information-rich
- visible flow between brief, AI output, and approval
- strong mobile and laptop responsiveness

## 9. Architecture Direction

### Backend

- FastAPI route layer
- service layer for agent workflows
- provider abstraction for LLM integrations
- typed schemas for contracts
- portable store layer for demo data, later replaceable with database persistence

### Frontend

- feature-oriented React structure
- API client wrapper
- stateful workspace shell
- reusable metric and workflow panels

## 10. Why Recruiters Will Like It

- Python delivery instead of notebook-only work
- agentic product design
- LLM-ready integration architecture
- business-facing AI use case
- polished frontend plus usable backend contract
- room to discuss evaluation, monitoring, and provider routing

## 11. Future Expansion

- model routing between providers
- retrieval over menus, events, and review archives
- publishing connectors for social and messaging channels
- approval analytics and output evaluation
- multi-brand portfolio views

