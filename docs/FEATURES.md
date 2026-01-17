# Features — Implementation Roadmap

> **Mission:** 80x faster, 2000x cheaper market research. Demo-ready for enterprise clients.

---

## Project Context

### Why We're Building This

We are an **AI systems and infrastructure consulting company**. This application is a **demo product** that showcases our capability to build enterprise-grade AI solutions. When a potential client sees this:

1. They should think: *"This is not a ChatGPT wrapper — this is real infrastructure."*
2. They should feel: *"If they can build this, they can build what I need."*
3. They should say: *"We want to work with this team."*

### What "Done" Looks Like

The final application should:

1. **Feel premium** — Visual polish matters. Source cards, progress pipelines, confidence meters.
2. **Be honest** — Show intelligence gaps, confidence levels. Transparency > overconfidence.
3. **Drive action** — Every report ends with prioritized recommendations.
4. **Allow control** — HITL checkpoints let users steer the research.
5. **Export professionally** — PDF with branding.

---

## Quick Reference

| Feature | Priority | Complexity |
|---------|----------|------------|
| F1. Research Type Selection | P0 | Medium |
| F2. Company Analysis | P0 | Low |
| F3. Competitive Comparison | P0 | Medium |
| F4. Confidence Scoring | P1 | Medium |
| F5. Source Freshness | P1 | Low |
| F6. Intelligence Gaps | P1 | Low |
| F7. Actionable Recommendations | P0 | Low |
| F8. HITL: Research Checkpoint | P1 | High |
| F9. PDF Export | P2 | Medium |

---

## Feature Specifications

---

### F1. Research Type Selection

**Summary:** Replace single "company + industry" input with research type selector.

**Icon:** `[mdi:format-list-bulleted-type]`

**Implementation:**
```typescript
enum ResearchType {
  COMPANY_ANALYSIS = "company_analysis",
  COMPETITIVE_COMPARISON = "competitive_comparison",
}
```

**UI Wireframe:**
```
+---------------------------------------------+
|  What do you need?                          |
|  ( ) [mdi:domain] Company Analysis          |
|  ( ) [mdi:compare] Competitive Comparison   |
+---------------------------------------------+
```

**Acceptance Criteria:**
- [ ] Radio button selection for research types
- [ ] Selection triggers dynamic input form (F2, F3)
- [ ] Default selection: Company Analysis
- [ ] Icons render correctly (Material Design Icons)

**Depends On:** None
**Blocks:** F2, F3

---

### F2. Company Analysis

**Summary:** Deep dive on a single company.

**Icon:** `[mdi:domain]`

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
- [ ] Form shows when `research_type == "company_analysis"`
- [ ] At least 10 cited sources in report
- [ ] Generation time <5 minutes
- [ ] SWOT section always present

**Depends On:** F1
**Blocks:** None

---

### F3. Competitive Comparison

**Summary:** Side-by-side comparison of 2-5 companies.

**Icon:** `[mdi:compare]`

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

**Depends On:** F1
**Blocks:** None

---

### F4. Confidence Scoring

**Summary:** Show confidence level on every claim.

**Icon:** `[mdi:shield-check]`

**Implementation:**
```typescript
enum ConfidenceLevel {
  HIGH = "high",      // 90%+ | green check
  MEDIUM = "medium",  // 70-89% | amber alert
  LOW = "low",        // <70% | red close
}
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
**Blocks:** None

---

### F5. Source Freshness

**Summary:** Show publication date on every source.

**Icon:** `[mdi:calendar-clock]`

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

### F6. Intelligence Gaps

**Summary:** Explicitly show what couldn't be found.

**Icon:** `[mdi:file-question]`

**Output Format:**
```
[mdi:clipboard-alert] Intelligence Gaps
- Pricing: Not publicly available
- Revenue: Estimated based on employee count
- Customer count: No reliable data found
```

**Acceptance Criteria:**
- [ ] Every report has gaps section
- [ ] Gaps explain what was tried
- [ ] Suggestions for filling gaps

**Depends On:** None
**Blocks:** None

---

### F7. Actionable Recommendations

**Summary:** Numbered next steps at end of every report.

**Icon:** `[mdi:clipboard-check]`

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

### F8. HITL: Research Checkpoint

**Summary:** Pause after research for user review.

**Icon:** `[mdi:account-check]`

**Flow:**
```
Research -> PAUSE -> User reviews sources -> Continue/Edit -> Analysis
```

**UI Wireframe:**
```
+---------------------------------------------+
|  [mdi:magnify] Research Complete            |
|                                             |
|  Sources Found: 15                          |
|  [mdi:plus] Add your own sources            |
|                                             |
|  +-------------------------------------+    |
|  | Source 1: TechCrunch (Dec 2024)     |    |
|  | Source 2: Forbes (Nov 2024)         |    |
|  | [mdi:delete] Remove                 |    |
|  +-------------------------------------+    |
|                                             |
|  [Continue to Analysis] [Auto-approve all]  |
+---------------------------------------------+
```

**Acceptance Criteria:**
- [ ] Workflow pauses after research node
- [ ] User can view all sources
- [ ] User can add/delete sources
- [ ] User can add notes
- [ ] Continue button resumes workflow

**Depends On:** None
**Blocks:** None

---

### F9. PDF Export

**Summary:** Export any report as PDF.

**Icon:** `[mdi:file-pdf-box]`

**Libraries:** `reportlab` (Python backend)

**Acceptance Criteria:**
- [ ] One-click PDF download
- [ ] Markdown rendered correctly
- [ ] Tables preserved
- [ ] Company branding/logo

**Depends On:** None
**Blocks:** None

---

## Dependency Graph

```
F1 (Research Type Selection)
├── F2 (Company Analysis)
└── F3 (Competitive Comparison)

F4 (Confidence Scoring) — standalone
F5 (Source Freshness) — standalone
F6 (Intelligence Gaps) — standalone
F7 (Actionable Recommendations) — standalone
F8 (HITL Research) — standalone
F9 (PDF Export) — standalone
```

---

## Personas (Reference)

| Persona | Primary Features | Time Budget |
|---------|-----------------|-------------|
| Product Manager | F2, F3, F7 | 30 min |
| Consultant | F2, F9 | 2 hours |

---

## Icon Reference

Using [Material Design Icons](https://materialdesignicons.com/):

| Purpose | Icon | Code |
|---------|------|------|
| Company | domain | `mdi:domain` |
| Compare | compare | `mdi:compare` |
| Check | check-circle | `mdi:check-circle` |
| Alert | alert-circle | `mdi:alert-circle` |
| Error | close-circle | `mdi:close-circle` |
| PDF | file-pdf-box | `mdi:file-pdf-box` |

---

*For postponed features (Market Landscape, Battle Card, Investment Thesis, Custom Query, additional HITL checkpoints, CSV export), see [FUTURE_FEATURES.md](./FUTURE_FEATURES.md)*

---

*Last updated: January 2025*
