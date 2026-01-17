# Future Features

> Features postponed from initial implementation. These will be considered after the first case study is complete and the core system is validated.

---

## Quick Reference

| Feature | Priority | Complexity | Original ID |
|---------|----------|------------|-------------|
| FF1. Market Landscape | P1 | High | F4 |
| FF2. Battle Card | P1 | Medium | F5 |
| FF3. Investment Thesis | P2 | High | F6 |
| FF4. Custom Query | P2 | Low | F7 |
| FF5. HITL: Analysis Checkpoint | P1 | High | F13 |
| FF6. HITL: Report Checkpoint | P1 | Medium | F14 |
| FF7. Battle Card 1-Pager PDF | P2 | Medium | F16 |
| FF8. CSV Data Export | P2 | Low | F17 |

---

## Feature Specifications

---

### FF1. Market Landscape

**Summary:** Full market overview with players, trends, and entry analysis.

**Icon:** `[mdi:earth]`

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

**Depends On:** F1 (Research Type Selection)

---

### FF2. Battle Card

**Summary:** 1-page sales enablement document.

**Icon:** `[mdi:sword-cross]`

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
- [ ] PDF export available

**Depends On:** F1 (Research Type Selection)
**Blocks:** FF7 (Battle Card 1-Pager PDF)

---

### FF3. Investment Thesis

**Summary:** Due diligence report for investors.

**Icon:** `[mdi:cash-multiple]`

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
- [ ] All claims show confidence

**Depends On:** F1, F4 (Confidence Scoring)

---

### FF4. Custom Query

**Summary:** Free-form research question.

**Icon:** `[mdi:help-circle]`

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

**Depends On:** F1 (Research Type Selection)

---

### FF5. HITL: Analysis Checkpoint

**Summary:** Pause after analysis for user review.

**Icon:** `[mdi:account-edit]`

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

**Depends On:** F8 (HITL: Research Checkpoint)
**Blocks:** FF6 (HITL: Report Checkpoint)

---

### FF6. HITL: Report Checkpoint

**Summary:** Pause after report for approval.

**Icon:** `[mdi:check-decagram]`

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

**Depends On:** FF5 (HITL: Analysis Checkpoint)

---

### FF7. Battle Card 1-Pager PDF

**Summary:** Condensed PDF format for battle cards.

**Icon:** `[mdi:card-account-details]`

**Acceptance Criteria:**
- [ ] Fits on single page
- [ ] Optimized for printing
- [ ] Key sections prominent
- [ ] QR code to full report (optional)

**Depends On:** FF2 (Battle Card), F9 (PDF Export)

---

### FF8. CSV Data Export

**Summary:** Export structured data for further analysis.

**Icon:** `[mdi:file-delimited]`

**Acceptance Criteria:**
- [ ] Comparison tables export as CSV
- [ ] Source list exports as CSV
- [ ] Key metrics export as CSV

**Depends On:** F3 (Competitive Comparison)

---

## Notes

These features are postponed to:
1. Keep initial implementation lean and focused
2. Enable faster first case study completion
3. Allow validation of core architecture before expanding
4. Support sequential evaluation approach

After the first case study is complete, these features will be prioritized based on learnings.

---

*Last updated: January 2025*
