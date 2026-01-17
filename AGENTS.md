# Project: Agentic Market Research

## Overview

Enterprise-grade AI-powered competitive intelligence system. Delivers comprehensive market research reports in minutes at <1% of traditional research costs.

## Stack

- **Frontend**: React 18 + Vite + Tailwind CSS + shadcn/ui
- **Backend**: Python 3.12 + FastAPI
- **PDF Generation**: reportlab
- **Package Management**: pnpm (frontend), uv (Python)
- **Deployment**: Vercel (frontend), Custom VPS (backend)

## Architecture

**Monorepo Structure:**
```
/frontend    # React SPA
/backend     # Python FastAPI
/docs        # Feature specs, future work
```

**Initial Approach:** Sequential processing for first case study. Optimization (Redis, aiohttp, Celery) planned for second iteration.

## Code Style

### Frontend (TypeScript/React)
- Functional components only
- Prefer composition over inheritance
- Use shadcn/ui components
- Material Design Icons (mdi) — never emoji
- Tailwind for styling, no CSS-in-JS

### Backend (Python)
- Strict typing (no `Any`)
- Async-first with FastAPI
- Pydantic for data validation
- ruff for linting, mypy for type checking

### Naming Conventions
- **Components**: PascalCase (`ResearchForm.tsx`)
- **Utilities**: camelCase (`formatDate.ts`)
- **Python modules**: snake_case (`market_analysis.py`)
- **API endpoints**: kebab-case (`/api/research-reports`)

## Common Commands

### Frontend
- **Dev**: `pnpm dev`
- **Build**: `pnpm build`
- **Lint**: `pnpm lint`
- **Type check**: `pnpm typecheck`

### Backend
- **Dev**: `uv run uvicorn app.main:app --reload`
- **Test**: `uv run pytest`
- **Lint**: `uv run ruff check .`
- **Type check**: `uv run mypy app/`

## Important Context

- **Purpose**: Demo product for AI consulting agency
- **Philosophy**: "Not a ChatGPT wrapper — real infrastructure"
- **Key differentiators**: Source cards, confidence scoring, intelligence gaps, HITL checkpoints
- **Case Study Approach**: Build sequential first, measure, then optimize

## Feature Implementation

See [docs/FEATURES.md](docs/FEATURES.md) for current scope (F1-F9).
See [docs/FUTURE_FEATURES.md](docs/FUTURE_FEATURES.md) for postponed features.

## Testing Philosophy

- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical user flows (after first case study)

## Notes

- First version is intentionally sequential for observation and case study creation
- Optimization phase comes after baseline is established
- Visual polish matters — this is a demo for enterprise clients
