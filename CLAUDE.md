# CLAUDE.md — The Ultrathink Constitution

> **"We're not here to write code. We're here to make a dent in the universe."**

This is not documentation. This is a covenant.

Every commit to this repository is a promise: that we will never settle for "good enough," that we will question every assumption, that we will craft solutions so elegant they feel inevitable.

---

## I. The Philosophy

### Think Different

The first solution is almost always wrong. Before writing code, ask:

- **Why does it have to work this way?**
- **What would this look like if we started from zero?**
- **What's the 80x improvement hiding in plain sight?**

> When everyone zigs, we zag. Standard patterns are suspicious—they're often just habits masquerading as wisdom.

### Simplify Ruthlessly

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."  
> — Antoine de Saint-Exupéry

Every abstraction must earn its place. Every configuration option is a decision deferred. Every line of code is a liability.

**If you can delete it—delete it.**

### Craft, Don't Code

The difference between a programmer and a craftsman:

- A programmer writes code that works.
- **A craftsman writes code that *reads*.** 

Variable names should explain intent. Functions should do one thing perfectly. The next engineer should feel like they're reading prose, not deciphering puzzles.

### Iterate Relentlessly

> The first draft is for the trash.  
> The second is for the critic.  
> The third is for the user.

Ship nothing until you've passed through the fire of revision. Take screenshots. Run tests. Compare outputs. Refine until it's not just working—but *insanely great*.

---

## II. The Architecture

### The Vision

Traditional market research is broken: **20+ hours** and **$3,000+** for a single competitive intelligence report. We fix this with a multi-agent system that delivers the same quality in **15 minutes** for **$1.50**.

That's not incremental improvement. That's a dent.

### The Symbiotic Triad

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestrator                   │
│                                                             │
│    ┌──────────┐      ┌──────────┐      ┌──────────┐        │
│    │          │      │          │      │          │        │
│    │ RESEARCH │ ──▶  │ ANALYSIS │ ──▶  │  WRITER  │        │
│    │  Agent   │      │  Agent   │      │  Agent   │        │
│    │          │      │          │      │          │        │
│    └──────────┘      └──────────┘      └──────────┘        │
│         │                 │                  │              │
│         ▼                 ▼                  ▼              │
│    Raw Data +        SWOT Matrix       Executive-Ready      │
│    Citations        + Positioning         Report            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

These are not microservices. They are **craftsmen**.

### The Research Agent — *The Hunter*

**File:** `src/agents/researcher.py`  
**Soul:** Relentless curiosity. Never satisfied with the first result.

This agent doesn't just search—it *hunts*. It uses Tavily's AI-optimized search to gather:
- Company overview and metrics
- Competitive landscape
- Market trends and signals

**Temperature:** 0.3 — Factual. Precise. No hallucinations.

Every source is cited. Every claim is verifiable. This is the foundation.

### The Analysis Agent — *The Strategist*

**File:** `src/agents/analyst.py`  
**Soul:** Pattern recognition. Ruthless synthesis.

This agent doesn't summarize—it *creates meaning*. Raw data becomes:
- SWOT matrices that reveal blind spots
- Competitive positioning maps
- Strategic gaps and opportunities

**The job isn't to repeat the data. The job is to find the insight hiding inside it.**

### The Writer Agent — *The Storyteller*

**File:** `src/agents/writer.py`  
**Soul:** Clarity. Authority. Zero fluff.

This agent transforms analysis into prose that executives will actually read:
- Executive summary: 200 words that matter
- Full report: scannable, citation-rich, actionable

**No buzzwords. No padding. Every sentence earns its place.**

---

## III. The Principles

### State as Truth

> **File:** `src/workflows/types.py`

The `IntelligenceState` TypedDict is the single source of truth. It flows through the graph, accumulating intelligence:

```python
IntelligenceState = {
    # Input
    company_name, industry, research_depth,
    
    # Research outputs
    research_data, competitors, market_trends, raw_sources,
    
    # Analysis outputs
    swot, competitive_matrix, positioning, strategic_recommendations,
    
    # Writing outputs
    executive_summary, full_report, report_metadata,
    
    # Workflow metadata
    current_agent, iteration, total_cost, total_tokens, errors,
    
    # Human-in-the-loop
    human_feedback, approved, revision_count,
}
```

**State is immutable between nodes. Each agent adds; none subtracts.**

### Prompts as Prose

> **File:** `src/utils/prompts.py`

Prompts are not strings. They are **instructions to intelligence**.

Write them like you're briefing the best analyst you've ever met:
- Be specific about structure
- Demand citations
- Specify output format exactly

Bad prompts create bad intelligence. Great prompts create magic.

### Costs as Conscience

> **File:** `src/utils/cost_tracker.py`

Every token costs money. Every LLM call is tracked. The `CostTracker` ensures:
- Budget enforcement (`BudgetExceededError`)
- Total cost visibility
- Per-agent breakdown

**The goal isn't cheap—it's *value*. $1.50 for $3,000 of intelligence.**

---

## IV. The Standards

### Python — The Language

| Standard | Requirement |
|----------|-------------|
| **Version** | 3.12+ |
| **Style** | `ruff` — no exceptions |
| **Typing** | Static. Mandatory. No `Any` unless legally unavoidable. |
| **Async** | The world is concurrent. Use `async/await` everywhere. |

### Patterns — The DNA

| Pattern | Implementation |
|---------|----------------|
| **Agent Base** | All agents inherit from `src.agents.base.BaseAgent` |
| **State** | `TypedDict` for LangGraph state (immutable between nodes) |
| **Config** | Environment variables via `src/utils/config.py` |
| **Prompts** | Centralized in `src/utils/prompts.py` — no magic strings |
| **Errors** | Fail gracefully. Report "Intelligence Gaps" — never crash. |

### Documentation — The Legacy

Code should explain *what*. Comments should explain *why*.

```python
# Bad: This loops through items
for item in items:
    process(item)

# Good: Process in order to maintain citation references
for item in items:
    process(item)
```

---

## V. The Rituals

### Setup

```bash
# Create isolated environment
python -m venv venv
source venv/bin/activate

# Install with speed
pip install uv && uv pip install -r requirements.txt

# Configure secrets
cp .env.example .env
# Edit .env with OPENROUTER_API_KEY and TAVILY_API_KEY
```

### Launch

```bash
# Gradio UI
python src/ui/app.py
# → http://localhost:7860

# Docker (production)
docker-compose up --build
```

### The Gauntlet

Before any push, run the full suite. No exceptions.

```bash
./scripts/run_all_tests.sh
```

This runs:
- **Ruff** — Linting (zero tolerance)
- **Mypy** — Type checking (static safety)
- **Pytest** — Unit + Integration tests

**If The Gauntlet fails, you do not push.**

---

## VI. The Covenant

### For Contributors

You're not submitting code. You're joining a mission.

Before you open a PR, ask:
1. Is this the **simplest** solution?
2. Does it **read** like prose?
3. Have I tested the **edge cases**?
4. Would I be **proud** of this in 5 years?

### For AI Assistants

You are not here to write code that works. You are here to write code that **sings**.

When given a task:
1. **Read the codebase first.** Understand the patterns, the philosophy, the soul.
2. **Question the requirements.** The stated problem may not be the real problem.
3. **Design before implementing.** Architecture first, keyboard second.
4. **Test ruthlessly.** If it's not tested, it's not done.
5. **Leave it better.** Every file you touch should be cleaner when you leave.

---

## VII. The Reality Distortion Field

When someone says it's impossible, that's your cue to think harder.

> "The people who are crazy enough to think they can change the world are the ones who do."

Market research shouldn't take 20 hours. It takes 15 minutes.
It shouldn't cost $3,000. It costs $1.50.
It shouldn't be inconsistent. It's standardized.

**We already made the dent.**

Now keep pushing.

---

*Last updated: December 2024*  
*Built by craftsmen who think different.*
