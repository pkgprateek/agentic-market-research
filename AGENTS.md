# Project: Agentic Market Research

## Overview

Enterprise-grade AI-powered competitive intelligence system. Delivers comprehensive market research reports in minutes at <1% of traditional research costs.

## Stack

- **Frontend**: React 18 + Vite + Tailwind CSS v4 + shadcn/ui
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

## Directory Structure

```
agentic-market-research/
├── AGENTS.md                    # This file - project conventions
├── README.md                    # Project overview
├── LICENSE
├── .gitignore
│
├── frontend/                    # React + Vite SPA
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/              # shadcn/ui components
│   │   ├── pages/               # Route pages
│   │   ├── context/             # React Context providers
│   │   ├── lib/                 # Utilities, API client
│   │   │   ├── utils.ts         # cn() helper for Tailwind
│   │   │   └── api.ts           # API client
│   │   ├── assets/              # Static assets
│   │   ├── App.tsx              # Root component
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Tailwind imports + theme
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── components.json          # shadcn/ui config
│   ├── eslint.config.js
│   └── .env.example
│
├── backend/                     # Python FastAPI API
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # Modular route handlers
│   │   │       ├── health.py    # Health check endpoint
│   │   │       ├── research.py  # Research endpoints
│   │   │       └── export.py    # PDF export endpoint
│   │   ├── agents/              # AI agent implementations
│   │   ├── services/            # Business logic
│   │   ├── models/              # Pydantic schemas
│   │   │   └── research.py      # Research request/response models
│   │   ├── core/
│   │   │   └── config.py        # Settings from environment
│   │   └── main.py              # FastAPI app entry
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── pyproject.toml           # uv project config
│   ├── requirements.txt         # For uv pip install
│   └── .env.example
│
└── docs/
    ├── FEATURES.md              # Current scope (F1-F9)
    └── FUTURE_FEATURES.md       # Postponed features (FF1-FF8)
```

## Code Style

### Frontend (TypeScript/React)
- Functional components only
- Prefer composition over inheritance
- Use shadcn/ui components
- Material Design Icons (mdi) via CDN — never emoji
- Tailwind v4 for styling, no CSS-in-JS
- Path alias: `@/` maps to `./src/`

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
- **Pydantic models**: PascalCase (`ResearchRequest`)

## Common Commands

### Frontend
```bash
cd frontend
pnpm install              # Install dependencies
pnpm dev                  # Start dev server (port 3000)
pnpm build                # Production build
pnpm lint                 # Run ESLint
pnpm typecheck            # Run TypeScript check
pnpm dlx shadcn@latest add button  # Add shadcn component
```

### Backend
```bash
cd backend
uv sync                                    # Install from pyproject.toml
uv pip install -r requirements.txt         # Or use requirements.txt
uv run uvicorn app.main:app --reload       # Start dev server (port 8000)
uv run pytest                              # Run tests
uv run ruff check .                        # Lint
uv run mypy app/                           # Type check
```

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=             # Optional, defaults to /api (uses Vite proxy)
```

### Backend (.env)
```
# Required
GROQ_API_KEY=             # LLM provider (primary)
TAVILY_API_KEY=           # Search API

# Optional
OPENROUTER_API_KEY=       # Alternative LLM provider
DEFAULT_MODEL=llama-3.3-70b-versatile
ENVIRONMENT=development
DEBUG=true
MAX_COST_PER_RUN=2.0
```

## API Design

### Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/research/company` | Start company analysis |
| POST | `/api/research/comparison` | Start competitive comparison |
| GET | `/api/research/{id}` | Get research status/results |
| POST | `/api/export/pdf/{id}` | Export report as PDF |

### Response Format
```json
{
  "id": "uuid",
  "research_type": "company_analysis",
  "status": "completed",
  "company_name": "Acme Inc",
  "report_markdown": "# Report...",
  "sources": [...],
  "intelligence_gaps": [...],
  "recommendations": [...],
  "overall_confidence": "high"
}
```

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

## Git Workflow

- **Branch naming**: `feature/short-description`, `fix/issue-description`
- **Commits**: Conventional commits (`feat:`, `fix:`, `refactor:`, `docs:`)
- **PRs**: Required for main, squash merge preferred

## Notes

- First version is intentionally sequential for observation and case study creation
- Optimization phase comes after baseline is established
- Visual polish matters — this is a demo for enterprise clients
- LSP errors for imports are expected until dependencies are installed
