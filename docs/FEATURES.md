# CLAUDE.md — Implementation Roadmap

> **Mission:** 80x faster, 2000x cheaper market research. Demo-ready for enterprise clients.

---

## Project Context (Read This First)

### Why We're Building This

We are an **AI systems and infrastructure consulting company**. This application is a **demo product** that showcases our capability to build enterprise-grade AI solutions. When a potential client sees this:

1. They should think: *"This is not a ChatGPT wrapper — this is real infrastructure."*
2. They should feel: *"If they can build this, they can build what I need."*
3. They should say: *"We want to work with this team."*

The market research problem is a vehicle. The real product is demonstrating **world-class execution**.

### Who Uses This

| Stakeholder | Role | What They Care About |
|-------------|------|---------------------|
| **End User (PM, Analyst)** | Runs research queries | Speed, accuracy, actionable insights |
| **Business Client** | Evaluates our agency | Technical sophistication, reliability |
| **Demo Viewer** | Sees live walkthrough | Visual polish, "wow factor", trust signals |
| **Internal (You, Agent)** | Builds the system | Code quality, maintainability, elegance |

### User Experience Philosophy

When implementing ANY feature, think through these lenses:

1. **End User Lens:** *"Does this save me time and give me confidence?"*
   - Fast feedback (progress pipeline, not spinners)
   - Transparent sources (I can verify claims)
   - Actionable output (what should I do next?)

2. **Business Client Lens:** *"Does this look enterprise-grade?"*
   - Professional visual design (not generic Gradio gray)
   - Sophisticated features (HITL, confidence scoring)
   - Attention to detail (MDI icons, not emoji)

3. **Demo Viewer Lens:** *"Am I impressed in 30 seconds?"*
   - Immediate visual impact
   - Clear value proposition visible
   - No awkward loading states

### What "Done" Looks Like

The final application should:

1. **Feel premium** — Visual polish matters. Source cards, progress pipelines, confidence meters.
2. **Be honest** — Show intelligence gaps, confidence levels. Transparency > overconfidence.
3. **Drive action** — Every report ends with prioritized recommendations.
4. **Allow control** — HITL checkpoints let users steer the research.
5. **Export professionally** — PDF with branding, CSV for analysis.

### Patterns From Best-in-Class Tools

We researched Perplexity, Consensus, and Elicit. Key differentiators:

| Pattern | What It Does | Why It Matters |
|---------|-------------|----------------|
| **Source Cards** | Visual cards for each source with metadata | Builds trust, scannable verification |
| **Progress Pipeline** | Stage-by-stage visual progress | Reduces perceived wait time |
| **Confidence Indicators** | Inline [High/Medium/Low] on claims | Honest uncertainty > false confidence |
| **Consensus Meter** | "85% of sources agree..." | Aggregated credibility signal |
| **Intelligence Gaps** | Explicit "we couldn't find..." | Transparency builds trust |
| **Actionable Recommendations** | Prioritized next steps | The "so what?" that PMs need |

### Technical Non-Negotiables

- **Python 3.12+** with strict typing (no `Any`)
- **Ruff** for linting, **mypy** for type checking
- **Material Design Icons** (`@mdi/font`) — never emoji
- **Async-first** architecture
- **Tests pass** before any merge (`make check`)

### The Dent

> "We're here to put a dent in the universe."

This is not about building a market research tool. It's about demonstrating that we execute at a level most agencies cannot match. Every line of code, every UI element, every interaction should reflect that standard.

---

## Quick Reference

| Feature | Status | Priority | Complexity |
|---------|--------|----------|------------|
| F1. Research Type Selection | [x] | P0 | Medium |
| F2. Company Analysis | [x] | P0 | Low |
| F3. Competitive Comparison | [ ] | P0 | Medium |
| F4. Market Landscape | [ ] | P1 | High |
| F5. Battle Card | [ ] | P1 | Medium |
| F6. Investment Thesis | [ ] | P2 | High |
| F7. Custom Query | [ ] | P2 | Low |
| F8. Confidence Scoring | [ ] | P1 | Medium |
| F9. Source Freshness | [ ] | P1 | Low |
| F10. Intelligence Gaps | [ ] | P1 | Low |
| F11. Actionable Recommendations | [ ] | P0 | Low |
| F12. HITL: Research Checkpoint | [ ] | P1 | High |
| F13. HITL: Analysis Checkpoint | [ ] | P1 | High |
| F14. HITL: Report Checkpoint | [ ] | P1 | Medium |
| F15. PDF Export | [ ] | P2 | Medium |
| F16. Battle Card 1-Pager | [ ] | P2 | Medium |
| F17. CSV Data Export | [ ] | P2 | Low |

---

## Feature Specifications

---

### F1. Research Type Selection

**Branch:** `feature/research-type-selection`

**Summary:** Replace single "company + industry" input with research type selector.

**Icon:** `[mdi:format-list-bulleted-type]`

**Files to Modify:**
- `src/ui/app.py` — New UI component
- `src/workflows/types.py` — Add `ResearchType` enum

**Implementation:**
```python
# src/workflows/types.py
class ResearchType(str, Enum):
    COMPANY_ANALYSIS = "company_analysis"
    COMPETITIVE_COMPARISON = "competitive_comparison"
    MARKET_LANDSCAPE = "market_landscape"
    BATTLE_CARD = "battle_card"
    INVESTMENT_THESIS = "investment_thesis"
    CUSTOM_QUERY = "custom_query"
```

**UI Wireframe:**
```
┌─────────────────────────────────────────────┐
│  What do you need?                          │
│  ○ [mdi:domain] Company Analysis            │
│  ○ [mdi:compare] Competitive Comparison     │
│  ○ [mdi:earth] Market Landscape             │
│  ○ [mdi:sword-cross] Battle Card            │
│  ○ [mdi:cash-multiple] Investment Thesis    │
│  ○ [mdi:help-circle] Custom Query           │
└─────────────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] Radio button selection for 6 research types
- [ ] Selection triggers dynamic input form (F2-F7)
- [ ] Default selection: Company Analysis
- [ ] Icons render correctly (Material Design Icons via CDN or local)

**Depends On:** None  
**Blocks:** F2, F3, F4, F5, F6, F7

---

### F2. Company Analysis

**Branch:** `feature/company-analysis`

**Summary:** Deep dive on a single company.

**Icon:** `[mdi:domain]`

**Files to Modify:**
- `src/ui/app.py` — Dynamic input form
- `src/utils/prompts.py` — Company-specific prompts
- `src/workflows/market_analysis.py` — Routing logic

**Inputs:**
| Field | Required | Type | Default |
|-------|----------|------|---------|
| Company Name | Yes | text | — |
| Industry | No | text | (inferred) |
| Focus Areas | No | checkboxes | All checked |

**Focus Areas Options:**
- [ ] Products & Services
- [ ] Pricing
- [ ] Leadership
- [ ] Financials
- [ ] Market Position

**Output Sections:**
1. Company Overview
2. Products & Services
3. Business Model
4. Key Metrics
5. SWOT Analysis
6. Market Position
7. Strategic Recommendations

**Acceptance Criteria:**
- [x] Form shows when `research_type == "company_analysis"`
- [x] At least 10 cited sources in report
- [x] Generation time <5 minutes
- [x] SWOT section always present

**Depends On:** F1  
**Blocks:** None

---

### F3. Competitive Comparison

**Branch:** `feature/competitive-comparison`

**Summary:** Side-by-side comparison of 2-5 companies.

**Icon:** `[mdi:compare]`

**Files to Modify:**
- `src/ui/app.py` — Multi-company input
- `src/utils/prompts.py` — Comparison prompts
- `src/agents/analyst.py` — Comparison logic

**Inputs:**
| Field | Required | Type | Default |
|-------|----------|------|---------|
| Your Company | Yes | text | — |
| Competitors | Yes | text[] (1-5) | — |
| Comparison Dimensions | No | checkboxes | All checked |

**Comparison Dimensions:**
- [ ] Features
- [ ] Pricing
- [ ] Market Share
- [ ] Technology
- [ ] Customer Segments

**Output Sections:**
1. Comparison Matrix (table)
2. Feature Analysis
3. Pricing Comparison
4. Competitive Advantages
5. Strategic Recommendations

**Acceptance Criteria:**
- [ ] Add/remove competitor buttons (max 5)
- [ ] Comparison table has all companies as columns
- [ ] Each dimension shows winner with rationale
- [ ] CSV export option for table data

**Depends On:** F1  
**Blocks:** None

---

### F4. Market Landscape

**Branch:** `feature/market-landscape`

**Summary:** Full market overview with players, trends, and entry analysis.

**Icon:** `[mdi:earth]`

**Files to Modify:**
- `src/ui/app.py` — Market input form
- `src/utils/prompts.py` — Market prompts
- `src/agents/researcher.py` — Market search queries

**Inputs:**
| Field | Required | Type | Default |
|-------|----------|------|---------|
| Market/Industry | Yes | text | — |
| Geography | No | dropdown | Global |
| Time Horizon | No | text | 2025-2027 |

**Output Sections:**
1. Market Overview (size, growth, drivers)
2. Key Players (top 10)
3. Market Segments
4. Trends & Predictions
5. PEST Analysis
6. Porter Five Forces
7. Entry Barriers & Opportunities

**Acceptance Criteria:**
- [ ] TAM/SAM/SOM estimates with methodology
- [ ] All players include market share or ranking
- [ ] Trends cite specific signals
- [ ] Porter diagram included

**Depends On:** F1  
**Blocks:** None

---

### F5. Battle Card

**Branch:** `feature/battle-card`

**Summary:** 1-page sales enablement document.

**Icon:** `[mdi:sword-cross]`

**Files to Modify:**
- `src/ui/app.py` — Battle card form
- `src/utils/prompts.py` — Battle card prompts
- `src/agents/writer.py` — Condensed output format

**Inputs:**
| Field | Required | Type | Default |
|-------|----------|------|---------|
| Your Company | Yes | text | — |
| Target Competitor | Yes | text | — |
| Deal Context | No | textarea | — |

**Output Sections:**
1. Quick Facts (side-by-side)
2. Why We Win (3-5 bullets)
3. Where They're Strong
4. Objection Handlers (5)
5. Proof Points
6. Knockout Punches

**Acceptance Criteria:**
- [ ] Fits on 1 page when printed
- [ ] Generation time <3 minutes
- [ ] Objection handlers are specific (not generic)
- [ ] PDF export available (F15)

**Depends On:** F1  
**Blocks:** F16

---

### F6. Investment Thesis

**Branch:** `feature/investment-thesis`

**Summary:** Due diligence report for investors.

**Icon:** `[mdi:cash-multiple]`

**Files to Modify:**
- `src/ui/app.py` — Investment form
- `src/utils/prompts.py` — Investment prompts
- `src/agents/analyst.py` — Risk analysis

**Inputs:**
| Field | Required | Type | Default |
|-------|----------|------|---------|
| Company Name | Yes | text | — |
| Investment Stage | No | dropdown | Series A |
| Thesis Hypothesis | No | textarea | — |

**Investment Stage Options:**
- Seed
- Series A
- Series B
- Series C+
- Growth

**Output Sections:**
1. Investment Recommendation (BUY/HOLD/PASS)
2. Company Deep Dive
3. Market Opportunity
4. Competitive Moat
5. Team Assessment
6. Financial Analysis
7. Risk Register (5+ risks)
8. Comparable Companies

**Acceptance Criteria:**
- [ ] Clear BUY/HOLD/PASS at top
- [ ] Risk register has mitigations
- [ ] Comparables include multiples
- [ ] All claims show confidence (F8)

**Depends On:** F1, F8  
**Blocks:** None

---

### F7. Custom Query

**Branch:** `feature/custom-query`

**Summary:** Free-form research question.

**Icon:** `[mdi:help-circle]`

**Files to Modify:**
- `src/ui/app.py` — Free-form input
- `src/utils/prompts.py` — Query prompts

**Inputs:**
| Field | Required | Type | Default |
|-------|----------|------|---------|
| Research Question | Yes | textarea | — |
| Context | No | textarea | — |

**Output Sections:**
1. Direct Answer
2. Supporting Evidence
3. Contrary Evidence
4. Confidence Assessment
5. Sources

**Acceptance Criteria:**
- [ ] Answers the specific question
- [ ] Shows both supporting AND contrary evidence
- [ ] Follow-up questions supported

**Depends On:** F1  
**Blocks:** None

---

### F8. Confidence Scoring

**Branch:** `feature/confidence-scoring`

**Summary:** Show confidence level on every claim.

**Icon:** `[mdi:shield-check]`

**Files to Modify:**
- `src/agents/base.py` — Confidence extraction
- `src/workflows/types.py` — Confidence model
- `src/ui/app.py` — Visual indicators

**Implementation:**
```python
class ConfidenceLevel(str, Enum):
    HIGH = "high"      # 90%+ | [mdi:check-circle] green
    MEDIUM = "medium"  # 70-89% | [mdi:alert-circle] amber
    LOW = "low"        # <70% | [mdi:close-circle] red
```

**Visual Format:**
```
Revenue is approximately $50M [mdi:check-circle] [High: 3 sources agree]
```

**Acceptance Criteria:**
- [ ] Confidence shown inline with claim
- [ ] Hover reveals sources
- [ ] Report summary shows overall confidence

**Depends On:** None  
**Blocks:** F6

---

### F9. Source Freshness

**Branch:** `feature/source-freshness`

**Summary:** Show publication date on every source.

**Icon:** `[mdi:calendar-clock]`

**Files to Modify:**
- `src/tools/search.py` — Extract dates
- `src/agents/writer.py` — Format dates

**Visual Format:**
```
Source: TechCrunch (Dec 2024) [mdi:check] Fresh
Source: Forbes (Mar 2023) [mdi:alert] Stale
```

| Freshness | Age | Indicator |
|-----------|-----|-----------|
| Fresh | <1 month | `[mdi:check]` green |
| Recent | 1-6 months | (none) |
| Stale | >6 months | `[mdi:alert]` amber |

**Acceptance Criteria:**
- [ ] All sources show date
- [ ] Stale sources flagged
- [ ] Report shows average age

**Depends On:** None  
**Blocks:** None

---

### F10. Intelligence Gaps

**Branch:** `feature/intelligence-gaps`

**Summary:** Explicitly show what couldn't be found.

**Icon:** `[mdi:file-question]`

**Files to Modify:**
- `src/agents/researcher.py` — Track gaps
- `src/workflows/types.py` — Gaps model
- `src/agents/writer.py` — Gaps section

**Output Format:**
```
[mdi:clipboard-alert] Intelligence Gaps
• Pricing: Not publicly available
• Revenue: Estimated based on employee count
• Customer count: No reliable data found
```

**Acceptance Criteria:**
- [ ] Every report has gaps section
- [ ] Gaps explain what was tried
- [ ] Suggestions for filling gaps

**Depends On:** None  
**Blocks:** None

---

### F11. Actionable Recommendations

**Branch:** `feature/actionable-recommendations`

**Summary:** Numbered next steps at end of every report.

**Icon:** `[mdi:clipboard-check]`

**Files to Modify:**
- `src/utils/prompts.py` — Recommendation prompts
- `src/agents/analyst.py` — Generate recommendations

**Output Format:**
```
[mdi:pin] Recommended Actions

1. [mdi:alert-octagon] [URGENT] Action with deadline
   Rationale: Why this matters now

2. [mdi:chess-queen] [STRATEGIC] Medium-term action
   Rationale: Strategic benefit

3. [mdi:eye] [MONITOR] Thing to watch
   Rationale: Potential future impact
```

**Acceptance Criteria:**
- [ ] 3-5 recommendations per report
- [ ] Each has priority tag
- [ ] Each has specific rationale

**Depends On:** None  
**Blocks:** None

---

### F12. HITL: Research Checkpoint

**Branch:** `feature/hitl-research`

**Summary:** Pause after research for user review.

**Icon:** `[mdi:account-check]`

**Files to Modify:**
- `src/workflows/market_analysis.py` — Checkpoint logic
- `src/ui/app.py` — Review UI

**Flow:**
```
Research → PAUSE → User reviews sources → Continue/Edit → Analysis
```

**UI Wireframe:**
```
┌─────────────────────────────────────────────┐
│  [mdi:magnify] Research Complete            │
│                                             │
│  Sources Found: 15                          │
│  [mdi:plus] Add your own sources            │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Source 1: TechCrunch (Dec 2024)     │    │
│  │ Source 2: Forbes (Nov 2024)         │    │
│  │ [mdi:delete] Remove                 │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  [Continue to Analysis] [Auto-approve all]  │
└─────────────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] Workflow pauses after research node
- [ ] User can view all sources
- [ ] User can add/delete sources
- [ ] User can add notes
- [ ] Continue button resumes workflow

**Depends On:** None  
**Blocks:** F13

---

### F13. HITL: Analysis Checkpoint

**Branch:** `feature/hitl-analysis`

**Summary:** Pause after analysis for user review.

**Icon:** `[mdi:account-edit]`

**Files to Modify:**
- `src/workflows/market_analysis.py` — Checkpoint logic
- `src/ui/app.py` — Edit UI

**Flow:**
```
Analysis → PAUSE → User reviews insights → Continue/Edit → Writing
```

**Acceptance Criteria:**
- [ ] Workflow pauses after analysis node
- [ ] User can view all insights
- [ ] User can edit/override conclusions
- [ ] User can add context
- [ ] Changes incorporated into report

**Depends On:** F12  
**Blocks:** F14

---

### F14. HITL: Report Checkpoint

**Branch:** `feature/hitl-report`

**Summary:** Pause after report for approval.

**Icon:** `[mdi:check-decagram]`

**Files to Modify:**
- `src/workflows/market_analysis.py` — Approval logic
- `src/ui/app.py` — Approval UI

**Flow:**
```
Writing → PAUSE → User reviews report → Approve/Revise
```

**Acceptance Criteria:**
- [ ] Workflow pauses after writing node
- [ ] User can request revisions
- [ ] Revision feedback sent to writer agent
- [ ] Audit trail of all revisions
- [ ] Final approval required

**Depends On:** F13  
**Blocks:** None

---

### F15. PDF Export

**Branch:** `feature/pdf-export`

**Summary:** Export any report as PDF.

**Icon:** `[mdi:file-pdf-box]`

**Files to Modify:**
- `src/ui/app.py` — Export button
- NEW: `src/utils/export.py` — PDF generation

**Libraries:** `weasyprint` or `pdfkit`

**Acceptance Criteria:**
- [ ] One-click PDF download
- [ ] Markdown rendered correctly
- [ ] Tables preserved
- [ ] Company branding/logo

**Depends On:** None  
**Blocks:** None

---

### F16. Battle Card 1-Pager

**Branch:** `feature/battlecard-pdf`

**Summary:** Condensed PDF format for battle cards.

**Icon:** `[mdi:card-account-details]`

**Files to Modify:**
- `src/utils/export.py` — 1-page template

**Acceptance Criteria:**
- [ ] Fits on single page
- [ ] Optimized for printing
- [ ] Key sections prominent
- [ ] QR code to full report (optional)

**Depends On:** F5, F15  
**Blocks:** None

---

### F17. CSV Data Export

**Branch:** `feature/csv-export`

**Summary:** Export structured data for further analysis.

**Icon:** `[mdi:file-delimited]`

**Files to Modify:**
- `src/ui/app.py` — CSV button
- NEW: `src/utils/export.py` — CSV generation

**Acceptance Criteria:**
- [ ] Comparison tables export as CSV
- [ ] Source list exports as CSV
- [ ] Key metrics export as CSV

**Depends On:** F3  
**Blocks:** None

---

## Dependency Graph

```
F1 (Research Type Selection)
├── F2 (Company Analysis)
├── F3 (Competitive Comparison) → F17 (CSV Export)
├── F4 (Market Landscape)
├── F5 (Battle Card) → F16 (1-Pager PDF)
├── F6 (Investment Thesis) ← F8 (Confidence)
└── F7 (Custom Query)

F8 (Confidence Scoring) → F6

F12 (HITL Research) → F13 (HITL Analysis) → F14 (HITL Report)

F15 (PDF Export) → F16 (1-Pager PDF)
```

---

## Personas (Reference)

| Persona | Primary Features | Time Budget |
|---------|-----------------|-------------|
| Product Manager | F2, F3, F11 | 30 min |
| Sales Rep | F5, F16 | 10 min |
| Consultant | F4, F15 | 2 hours |
| Investor | F6, F8 | 1 hour |

---

## Technical Standards

| Standard | Value |
|----------|-------|
| Python | 3.12+ |
| Linting | `ruff` |
| Types | Static, no `Any` |
| Async | `async/await` |
| Tests | `make check` |
| Icons | Material Design Icons (`@mdi/font`) |

---

## Icon Reference

Using [Material Design Icons](https://materialdesignicons.com/):

| Purpose | Icon | Code |
|---------|------|------|
| Company | domain | `mdi:domain` |
| Compare | compare | `mdi:compare` |
| Market | earth | `mdi:earth` |
| Battle | sword-cross | `mdi:sword-cross` |
| Investment | cash-multiple | `mdi:cash-multiple` |
| Query | help-circle | `mdi:help-circle` |
| Check | check-circle | `mdi:check-circle` |
| Alert | alert-circle | `mdi:alert-circle` |
| Error | close-circle | `mdi:close-circle` |
| PDF | file-pdf-box | `mdi:file-pdf-box` |
| CSV | file-delimited | `mdi:file-delimited` |

---

## UI Research: Best-in-Class Patterns

> Research conducted on leading AI research tools to identify patterns that differentiate enterprise-grade products.

### Competitive Analysis

| Tool | Strength | Why Users Prefer It |
|------|----------|---------------------|
| **Perplexity** | Visual source cards, streaming UI, transparent citations | Feels fast, shows work, builds trust |
| **Consensus** | Consensus meter, inline citations, study snapshots | Academic credibility, at-a-glance synthesis |
| **Elicit** | Living documents, editable tables, confidence flags | Research workflow integration, control |
| **ChatGPT** | Simple chat, familiar interface | Low learning curve |

### Patterns We Should Implement

#### 1. Source Cards (High Priority)
Instead of plain text citations, show sources as visual cards:
```
┌─────────────────────────────────────────────────────────┐
│ [mdi:newspaper] TechCrunch                  Dec 2024   │
│ "Tesla's Q4 deliveries beat expectations..."            │
│ [mdi:check] Fresh  |  [mdi:shield-check] High Confidence│
└─────────────────────────────────────────────────────────┘
```
**Why:** Enterprise clients need to verify sources. Cards make this scannable.

#### 2. Progress Pipeline (Medium Priority)
Replace text status with visual pipeline:
```
[Research] ━━━━━● [Analysis] ━━━━━○ [Writing] ━━━━━○ [Review]
     ✓              In Progress
```
**Why:** Users perceive progress as faster when they see stages. Reduces perceived wait time.

#### 3. Confidence Visualization (High Priority - F8)
Inline indicators on every claim:
```
Revenue is approximately $50M [mdi:check-circle green] High: 3 sources agree
Market share is ~15% [mdi:alert-circle amber] Medium: conflicting reports
```
**Why:** Enterprise decisions require confidence levels. Honest uncertainty > false confidence.

#### 4. Consensus Meter (Medium Priority)
Show agreement across sources:
```
┌─────────────────────────────────────────────────────────┐
│  Market Position Consensus                              │
│  ████████████░░░░░░░░  85% sources agree: "Leader"     │
└─────────────────────────────────────────────────────────┘
```
**Why:** Aggregated view builds confidence in AI-generated insights.

#### 5. Intelligence Gaps Section (High Priority - F10)
Explicit about what wasn't found:
```
[mdi:file-question] Intelligence Gaps
• Pricing: Not publicly available (checked 12 sources)
• Revenue: Estimated from employee count (±30% accuracy)
• Customer count: No reliable data found
```
**Why:** Transparency about limitations builds trust. Enterprise clients respect honesty.

#### 6. Actionable Recommendations (High Priority - F11)
Prioritized next steps:
```
[mdi:pin] Recommended Actions

1. [URGENT] Monitor Q1 earnings call — rationale
2. [STRATEGIC] Evaluate partnership opportunity — rationale  
3. [MONITOR] Track competitor's new product launch — rationale
```
**Why:** Research without action recommendations is incomplete. PMs need "so what?"

---

### Why This Matters for Our Agency

| What Most Agencies Do | What We Do |
|----------------------|------------|
| Plain text reports | Visual source cards, confidence meters |
| "Processing..." spinner | Stage-by-stage progress pipeline |
| Hide limitations | Explicit intelligence gaps |
| Generic insights | Actionable recommendations with priority |
| One-shot output | HITL checkpoints for refinement |

**The Dent:** When a PM or consultant sees our output, they should immediately recognize this is not a ChatGPT wrapper — it's enterprise-grade research infrastructure.

---

## Known Issues (Post-Implementation)

### UI/UX

| Issue | Priority | Status |
|-------|----------|--------|
| MDI icons not inline in radio labels | Low | Gradio limitation, icons in description |
| Source cards not implemented | High | Pending F2 completion |
| Confidence visualization | High | Blocked by F8 |
| Progress pipeline | Medium | Current: text status |
| Consensus meter | Medium | Future enhancement |

### Technical

| Issue | Priority | Status |
|-------|----------|--------|
| Gradio 6.0 compatibility | Low | Using minimal gr.Blocks() |
| Model options hardcoded | Low | In app.py, consider config |

---

*Last updated: January 2025*

