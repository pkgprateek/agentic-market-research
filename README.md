# Agentic Market Research

> **Enterprise-grade AI-powered competitive intelligence.**  
> 80x faster, 2000x cheaper than manual research.

---

## Overview

The **Agentic Market Research** system automates competitive market analysis through orchestrated AI agents. Enter a company name, get a comprehensive intelligence report in minutes.

**Value Proposition:**
- **Speed:** 20+ hours → ~15 minutes (80x faster)
- **Cost:** ~$3,000 → $0.50-$2.00 per report (1500x cheaper)
- **Consistency:** Standardized, reproducible outputs

## Architecture

```
Frontend (Vercel)          Backend (VPS)
+------------------+       +------------------+
| React 18 + Vite  | <---> | Python 3.12      |
| Tailwind CSS     |       | FastAPI          |
| shadcn/ui        |       | AI Agents        |
+------------------+       +------------------+
                                   |
                                   v
                           +------------------+
                           | LLM APIs         |
                           | Search APIs      |
                           +------------------+
```

## Tech Stack

### Frontend (Vercel)
- React 18 (no Next.js)
- Vite
- Tailwind CSS
- shadcn/ui
- Material Design Icons (mdi)
- React Router
- Context API

### Backend (VPS)
- Python 3.12
- FastAPI
- reportlab (PDF generation)
- mypy (type checking)
- pytest (testing)

### Package Management
- pnpm (frontend)
- uv (Python)

## Project Structure

```
agentic-market-research/
├── frontend/           # React + Vite application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   └── lib/
│   └── package.json
├── backend/            # Python FastAPI application
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   ├── services/
│   │   └── models/
│   └── pyproject.toml
├── docs/               # Documentation
│   ├── FEATURES.md
│   └── FUTURE_FEATURES.md
└── AGENTS.md           # Project rules and conventions
```

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.12+
- pnpm
- uv

### Development

```bash
# Frontend
cd frontend
pnpm install
pnpm dev

# Backend
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

## Features

See [docs/FEATURES.md](docs/FEATURES.md) for implementation roadmap.

**Current Scope (9 features):**
1. Research Type Selection
2. Company Analysis
3. Competitive Comparison
4. Confidence Scoring
5. Source Freshness
6. Intelligence Gaps
7. Actionable Recommendations
8. HITL: Research Checkpoint
9. PDF Export

**Future Features:** See [docs/FUTURE_FEATURES.md](docs/FUTURE_FEATURES.md)

## License

MIT

---

**Built by Prateek Kumar Goel**
