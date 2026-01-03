# Missed Opportunities — Features for Best-in-Class Market Research

> **Note:** These are features observed in leading tools (Perplexity, Consensus, Elicit) that would elevate the application to industry-leading standards. Consider prioritizing based on client feedback and market demand.

---

## Priority 1 — Core User Experience Enhancements

### 1. Real-Time Streaming Results
**What:** Show research results as they're discovered, not just at the end.

**Why:** Perplexity's streaming UI makes users feel progress immediately. Reduces perceived wait time by 40-60%.

**Implementation:**
```python
# Stream sources as they're discovered
async def stream_sources():
    for source in research_agent.discover_sources():
        yield render_source_card(source)  # Update UI incrementally
```

**Complexity:** Medium  
**Impact:** High

---

### 2. Inline Citation Hover
**What:** Hover over any claim in the report to see which sources support it.

**Why:** Elicit's inline citations build trust. Users can verify claims instantly without scrolling to sources.

**Implementation:**
```html
Revenue is $96.8B <span class="citation-badge" data-sources="1,3,5">[3]</span>

<!-- Hover tooltip -->
<div class="citation-tooltip">
  <div class="source-link">Tesla Q4 2024 Earnings Report</div>
  <div class="source-link">EV Market Analysis 2024</div>
  <div class="source-link">Global EV Sales Data</div>
</div>
```

**Complexity:** Medium  
**Impact:** High

---

### 3. Follow-Up Questions
**What:** Suggest related research queries based on current report.

**Why:** Consensus's "Related Studies" feature increases engagement. Users often want to dive deeper.

**Implementation:**
```python
def generate_followup_questions(report: str) -> list[str]:
    """Generate 3-5 follow-up questions based on report content."""
    prompt = f"""
    Based on this report about {company_name}, suggest 3-5 follow-up questions
    that would provide additional valuable insights.
    
    Report: {report}
    """
    return llm.generate(prompt)
```

**Complexity:** Low  
**Impact:** Medium

---

### 4. Source Verification Flags
**What:** Allow users to flag sources as reliable/unreliable, influencing future research.

**Why:** Builds community trust. Consensus lets users vote on source quality.

**Implementation:**
```python
class SourceRating:
    source_id: str
    user_id: str
    rating: Literal["reliable", "unreliable", "mixed"]
    timestamp: datetime
```

**Complexity:** High (requires user accounts, database)  
**Impact:** Medium

---

## Priority 2 — Advanced Research Features

### 5. Historical Report Comparison
**What:** Compare reports for the same company over time to track changes.

**Why:** PMs need to track competitive evolution. "How has Tesla's position changed since Q2?"

**Implementation:**
```python
def compare_reports(report_a: Report, report_b: Report) -> ComparisonResult:
    """Highlight differences between two reports."""
    return {
        "new_insights": [...],
        "changed_metrics": [...],
        "disappeared_insights": [...],
    }
```

**Complexity:** Medium  
**Impact:** High

---

### 6. Sentiment Analysis Timeline
**What:** Track sentiment around companies/markets over time with visual charts.

**Why:** Elicit's sentiment tracking helps identify trends. "Tesla sentiment dropped 15% after price cuts."

**Implementation:**
```python
def plot_sentiment_timeline(company: str, days: int = 90):
    """Generate sentiment chart from news/social data."""
    data = sentiment_analyzer.get_timeline(company, days)
    return render_chart(data)
```

**Complexity:** High  
**Impact:** High

---

### 7. Competitor Monitoring Dashboard
**What:** Ongoing monitoring view with alerts for key events (funding, product launches, etc.).

**Why:** PMs need to stay informed without running full reports daily.

**Implementation:**
```python
class CompetitorMonitor:
    """Track competitors and alert on key events."""
    
    def setup_alerts(self, company: str, event_types: list[str]):
        """Set up alerts for funding, launches, leadership changes, etc."""
        pass
    
    def get_dashboard(self) -> Dashboard:
        """Return monitoring dashboard with recent events."""
        pass
```

**Complexity:** High  
**Impact:** High

---

### 8. Advanced Source Filtering
**What:** Filter sources by date range, source type (news, academic, social), reliability score.

**Why:** Perplexity lets users filter by time. "Only show sources from last 30 days."

**Implementation:**
```python
def filter_sources(
    sources: list[Source],
    date_range: tuple[datetime, datetime],
    source_types: list[str],
    min_reliability: float,
) -> list[Source]:
    """Filter sources based on criteria."""
    pass
```

**Complexity:** Low  
**Impact:** Medium

---

## Priority 3 — Enterprise Features

### 9. CRM Integration
**What:** Push insights directly to Salesforce, HubSpot, or other CRM systems.

**Why:** Enterprise clients want research in their existing workflows.

**Implementation:**
```python
def export_to_crm(report: Report, crm: str, account_id: str):
    """Export report insights to CRM system."""
    if crm == "salesforce":
        salesforce_api.create_note(account_id, report.summary)
    elif crm == "hubspot":
        hubspot_api.create_engagement(account_id, report.summary)
```

**Complexity:** Medium  
**Impact:** High (for enterprise clients)

---

### 10. White-Label Reports
**What:** Customize reports with company branding, logo, and templates.

**Why:** Consulting firms need to deliver branded reports to clients.

**Implementation:**
```python
def generate_branded_pdf(
    report: Report,
    company_logo: str,
    template: str,
) -> bytes:
    """Generate PDF with custom branding."""
    pass
```

**Complexity:** Medium  
**Impact:** High (for consulting clients)

---

### 11. Collaboration Features
**What:** Share reports with team, add comments, track revisions.

**Why:** Teams collaborate on research. "Can you review this Tesla report?"

**Implementation:**
```python
class SharedReport:
    report_id: str
    owner_id: str
    shared_with: list[str]
    comments: list[Comment]
    revision_history: list[Revision]
```

**Complexity:** High  
**Impact:** High

---

### 12. Report Templates
**What:** Pre-built templates for common use cases (investor pitch, sales call, board meeting).

**Why:** Saves time. "Generate investor-ready report template."

**Implementation:**
```python
TEMPLATES = {
    "investor_pitch": {
        "sections": ["executive_summary", "market_opportunity", "competitive_moat", "financials"],
        "tone": "confident, data-driven",
    },
    "sales_call": {
        "sections": ["key_differentiators", "objection_handlers", "proof_points"],
        "tone": "persuasive, concise",
    },
}
```

**Complexity:** Low  
**Impact:** Medium

---

## Priority 4 — Advanced Analytics

### 13. Market Size Calculator
**What:** Interactive TAM/SAM/SOM calculator with methodology explanations.

**Why:** PMs need market sizing. "What's the addressable market for EVs in Europe?"

**Implementation:**
```python
def calculate_market_size(
    total_market: float,
    serviceable_market: float,
    obtainable_market: float,
    methodology: str,
) -> MarketSizeResult:
    """Calculate TAM/SAM/SOM with methodology."""
    return {
        "tam": total_market,
        "sam": serviceable_market,
        "som": obtainable_market,
        "methodology": methodology,
    }
```

**Complexity:** Medium  
**Impact:** High

---

### 14. Porter's Five Forces Interactive
**What:** Interactive Porter's Five Forces diagram with drag-and-drop ratings.

**Why:** Visual analysis is more engaging. Elicit has interactive diagrams.

**Implementation:**
```python
def render_porters_five_forces(company: str) -> str:
    """Generate interactive Porter's diagram."""
    forces = analyze_porters_forces(company)
    return render_interactive_diagram(forces)
```

**Complexity:** High  
**Impact:** Medium

---

### 15. Scenario Planning
**What:** Generate scenarios (bull case, bear case, base case) with probabilities.

**Why:** Investors need scenario analysis. "What if BYD enters US market?"

**Implementation:**
```python
def generate_scenarios(company: str) -> list[Scenario]:
    """Generate bull/base/bear scenarios."""
    return [
        Scenario("Bull", probability=0.25, assumptions=[...]),
        Scenario("Base", probability=0.50, assumptions=[...]),
        Scenario("Bear", probability=0.25, assumptions=[...]),
    ]
```

**Complexity:** High  
**Impact:** High (for investors)

---

## Priority 5 — Technical Enhancements

### 16. API Access
**What:** RESTful API for programmatic access to research capabilities.

**Why:** Enterprise clients want to integrate into their own applications.

**Implementation:**
```python
# FastAPI endpoints
@app.post("/api/v1/research")
async def run_research(request: ResearchRequest) -> ResearchResponse:
    """Run research via API."""
    pass

@app.get("/api/v1/reports/{report_id}")
async def get_report(report_id: str) -> Report:
    """Retrieve report by ID."""
    pass
```

**Complexity:** Medium  
**Impact:** High (for enterprise clients)

---

### 17. Multi-Language Support
**What:** Generate reports in multiple languages (English, Spanish, German, etc.).

**Why:** Global clients need reports in their language.

**Implementation:**
```python
def translate_report(report: Report, target_language: str) -> Report:
    """Translate report to target language."""
    pass
```

**Complexity:** Medium  
**Impact:** Medium

---

### 18. Voice Input
**What:** Dictate research queries using speech-to-text.

**Why:** Mobile users prefer voice input. Perplexity has voice search.

**Implementation:**
```python
def transcribe_voice(audio_file: bytes) -> str:
    """Transcribe audio to text."""
    return whisper_api.transcribe(audio_file)
```

**Complexity:** Low  
**Impact:** Low

---

### 19. Mobile App
**What:** Native mobile application for iOS and Android.

**Why:** PMs need research on-the-go.

**Complexity:** Very High  
**Impact:** Medium

---

### 20. Offline Mode
**What:** Cache reports and sources for offline viewing.

**Why:** Users may not always have internet access.

**Complexity:** Medium  
**Impact:** Low

---

## Summary by Priority

| Priority | Features | Total Impact |
|----------|----------|--------------|
| **P1** | Streaming, Citation Hover, Follow-up Questions, Source Flags | High |
| **P2** | Historical Comparison, Sentiment Timeline, Monitoring Dashboard, Source Filtering | High |
| **P3** | CRM Integration, White-Label Reports, Collaboration, Templates | High |
| **P4** | Market Size Calculator, Porter's Five Forces, Scenario Planning | High |
| **P5** | API Access, Multi-Language, Voice Input, Mobile App, Offline Mode | Medium |

---

## Recommended Implementation Order

**Phase 1 (Quick Wins - 1-2 weeks):**
1. Follow-up Questions
2. Source Filtering
3. Report Templates

**Phase 2 (Core Enhancements - 1 month):**
4. Real-Time Streaming
5. Inline Citation Hover
6. Historical Report Comparison

**Phase 3 (Enterprise Features - 2 months):**
7. CRM Integration
8. White-Label Reports
9. API Access

**Phase 4 (Advanced Analytics - 3 months):**
10. Market Size Calculator
11. Sentiment Analysis Timeline
12. Scenario Planning

**Phase 5 (Long-term - 6+ months):**
13. Collaboration Features
14. Competitor Monitoring Dashboard
15. Mobile App

---

## Competitive Analysis Summary

| Feature | Perplexity | Consensus | Elicit | Our App |
|---------|------------|-----------|--------|---------|
| Real-Time Streaming | ✅ | ❌ | ✅ | ❌ |
| Citation Hover | ❌ | ✅ | ✅ | ❌ |
| Follow-up Questions | ✅ | ✅ | ❌ | ❌ |
| Source Verification | ❌ | ✅ | ❌ | ❌ |
| Historical Comparison | ❌ | ❌ | ❌ | ❌ |
| Sentiment Analysis | ❌ | ❌ | ✅ | ❌ |
| CRM Integration | ❌ | ❌ | ❌ | ❌ |
| White-Label Reports | ❌ | ❌ | ❌ | ❌ |
| Collaboration | ❌ | ❌ | ❌ | ❌ |
| API Access | ❌ | ❌ | ❌ | ❌ |

**Conclusion:** We have strong differentiation in HITL checkpoints and confidence scoring, but lag in real-time UX and enterprise features. Implementing P1-P3 features would put us ahead of competitors.

---

*Last updated: January 2025*
