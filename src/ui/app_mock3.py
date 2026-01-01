"""Enterprise-Grade UI Mock v3 — Best of Both Designs.

Combines:
- am1: Header style, research type cards, contained sections, colors
- am2: Tabs for Report/Sources, centered progress, clean spacing

Run: python -m src.ui.app_mock3
Port: 7864
"""

import gradio as gr

# ─────────────────────────────────────────────────────────────────────────────
# Design System — Refined Dark Theme
# ─────────────────────────────────────────────────────────────────────────────

COLORS = {
    # Base - Sophisticated dark (from am1)
    "bg_primary": "#0a0a0c",
    "bg_secondary": "#131316",
    "bg_elevated": "#1a1a1f",
    "bg_card": "#16161a",
    # Borders
    "border": "#2a2a33",
    "border_accent": "#3d3d4a",
    # Text
    "text_primary": "#f4f4f5",
    "text_secondary": "#a1a1aa",
    "text_muted": "#71717a",
    # Accent - Teal (from am1)
    "accent": "#14b8a6",
    "accent_hover": "#2dd4bf",
    "accent_muted": "rgba(20, 184, 166, 0.15)",
    # Semantic
    "success": "#10b981",
    "success_bg": "rgba(16, 185, 129, 0.15)",
    "warning": "#f59e0b",
    "warning_bg": "rgba(245, 158, 11, 0.15)",
    "error": "#ef4444",
    "error_bg": "rgba(239, 68, 68, 0.15)",
    "info": "#3b82f6",
    "info_bg": "rgba(59, 130, 246, 0.15)",
    # Gradients
    "gradient_accent": "linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)",
    "gradient_header": "linear-gradient(135deg, #131316 0%, #0a0a0c 100%)",
}

MDI_CDN = (
    "https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Premium Theme (Best of Both)
# ─────────────────────────────────────────────────────────────────────────────

THEME_CSS = f"""
* {{ box-sizing: border-box; }}

.gradio-container {{
    background: {COLORS["bg_primary"]} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {COLORS["text_primary"]} !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}}

.dark, .gr-form, .gr-box, .gr-panel {{
    background: {COLORS["bg_primary"]} !important;
}}

/* Typography */
h1, h2, h3, h4 {{
    color: {COLORS["text_primary"]} !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}}

label {{
    color: {COLORS["text_secondary"]} !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}}

/* Form Elements */
input, textarea, select {{
    background: {COLORS["bg_secondary"]} !important;
    border: 1px solid {COLORS["border"]} !important;
    color: {COLORS["text_primary"]} !important;
    border-radius: 10px !important;
    padding: 0.875rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.2s !important;
}}

input:focus, textarea:focus {{
    border-color: {COLORS["accent"]} !important;
    box-shadow: 0 0 0 3px {COLORS["accent_muted"]} !important;
    outline: none !important;
}}

/* Buttons */
button.primary {{
    background: {COLORS["gradient_accent"]} !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.875rem 1.75rem !important;
    box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3) !important;
    transition: all 0.2s !important;
}}

button.primary:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(20, 184, 166, 0.4) !important;
}}

/* Cards - Contained sections (from am1) */
.card {{
    background: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 14px;
    padding: 1.5rem;
    transition: all 0.2s;
}}

.card:hover {{
    border-color: {COLORS["border_accent"]};
}}

.card-selected {{
    border-color: {COLORS["accent"]} !important;
    background: {COLORS["accent_muted"]} !important;
}}

/* Research Type Cards (from am1) */
.research-card {{
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 1.25rem;
    cursor: pointer;
    transition: all 0.2s;
}}

.research-card:hover {{
    border-color: {COLORS["accent"]};
    background: {COLORS["bg_elevated"]};
    transform: translateY(-2px);
}}

.research-card.active {{
    border-color: {COLORS["accent"]};
    background: {COLORS["accent_muted"]};
}}

/* Source Cards */
.source-card {{
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 1.25rem;
    margin: 0.75rem 0;
    transition: all 0.2s;
}}

.source-card:hover {{
    border-color: {COLORS["accent"]};
}}

/* Progress (centered, from am2) */
.progress-container {{
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
}}

.progress-bar {{
    height: 4px;
    background: {COLORS["border"]};
    border-radius: 2px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    background: {COLORS["gradient_accent"]};
    border-radius: 2px;
    animation: pulse 2s infinite;
}}

/* Badges */
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.375rem 0.75rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}}

.badge-success {{ background: {COLORS["success_bg"]}; color: {COLORS["success"]}; }}
.badge-warning {{ background: {COLORS["warning_bg"]}; color: {COLORS["warning"]}; }}
.badge-error {{ background: {COLORS["error_bg"]}; color: {COLORS["error"]}; }}
.badge-info {{ background: {COLORS["info_bg"]}; color: {COLORS["info"]}; }}

/* Confidence */
.confidence-high {{ color: {COLORS["success"]}; }}
.confidence-medium {{ color: {COLORS["warning"]}; }}
.confidence-low {{ color: {COLORS["error"]}; }}

/* Consensus Meter */
.consensus-meter {{
    background: {COLORS["bg_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}}

.consensus-bar {{
    height: 8px;
    background: {COLORS["border"]};
    border-radius: 4px;
    overflow: hidden;
}}

.consensus-fill {{
    height: 100%;
    background: {COLORS["gradient_accent"]};
    border-radius: 4px;
}}

/* HITL Checkpoint (from am2, cleaned) */
.hitl-checkpoint {{
    background: {COLORS["accent_muted"]};
    border: 2px solid {COLORS["accent"]};
    border-radius: 14px;
    padding: 1.75rem;
    margin: 2rem 0;
}}

/* Section Headers */
.section-header {{
    display: flex;
    align-items: center;
    gap: 0.625rem;
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 1.25rem;
    color: {COLORS["text_primary"]};
}}

/* Export Buttons (centered, with colors from am1) */
.export-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
}}

.export-pdf {{ background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; }}
.export-csv {{ background: linear-gradient(135deg, #16a34a, #15803d); color: white; }}
.export-copy {{ background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]}; }}
.export-share {{ background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; }}

/* Report Content (markdown formatting) */
.report-content {{
    color: {COLORS["text_primary"]};
    line-height: 1.75;
}}

.report-content h2 {{
    color: {COLORS["text_primary"]};
    margin-top: 2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {COLORS["border"]};
}}

.report-content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
}}

.report-content th, .report-content td {{
    padding: 0.875rem 1rem;
    text-align: left;
    border-bottom: 1px solid {COLORS["border"]};
}}

.report-content th {{
    background: {COLORS["bg_elevated"]};
    color: {COLORS["text_muted"]};
    font-weight: 600;
    font-size: 0.875rem;
    text-transform: uppercase;
}}

/* Gap Section */
.gaps-section {{
    background: {COLORS["warning_bg"]};
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    padding: 1.25rem;
    border-top: 3px solid {COLORS["warning"]};
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {COLORS["bg_primary"]}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS["border"]}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {COLORS["border_accent"]}; }}

/* Animations */
@keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}

/* Tabs - aligned with content */
.tabs {{
    border-bottom: 1px solid {COLORS["border"]} !important;
    margin-bottom: 1.5rem !important;
}}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Mock Data
# ─────────────────────────────────────────────────────────────────────────────

RESEARCH_TYPES = [
    (
        "Company Analysis",
        "domain",
        "Deep dive on a single company — products, SWOT, positioning",
    ),
    ("Competitive Comparison", "compare", "Side-by-side comparison of 2-5 competitors"),
    (
        "Market Landscape",
        "earth",
        "Full market overview with players, trends, and sizing",
    ),
    ("Battle Card", "sword-cross", "1-page sales enablement document"),
    ("Investment Thesis", "cash-multiple", "Due diligence report for investors"),
    ("Custom Query", "help-circle", "Free-form research question"),
]

MOCK_SOURCES = [
    {
        "title": "Tesla Q4 2024 Earnings Report",
        "source": "Tesla IR",
        "date": "Jan 2025",
        "freshness": "fresh",
        "confidence": "high",
        "snippet": "Tesla delivered 1.8M vehicles in 2024, up 38% YoY. Automotive gross margin at 16.3%.",
    },
    {
        "title": "Global EV Market Analysis",
        "source": "BloombergNEF",
        "date": "Dec 2024",
        "freshness": "fresh",
        "confidence": "high",
        "snippet": "Global EV sales reached 14.1M units in 2024, representing 18% of total auto sales.",
    },
    {
        "title": "Tesla vs BYD Competition",
        "source": "Reuters",
        "date": "Dec 2024",
        "freshness": "fresh",
        "confidence": "medium",
        "snippet": "BYD overtook Tesla in quarterly deliveries for the first time in Q4 2024.",
    },
    {
        "title": "Battery Technology Trends",
        "source": "MIT Tech Review",
        "date": "Sep 2024",
        "freshness": "recent",
        "confidence": "medium",
        "snippet": "4680 cell production at Gigafactory Texas reached 10 GWh annual capacity.",
    },
]

MOCK_GAPS = [
    {
        "topic": "Exact gross margin by product line",
        "reason": "Not disclosed in public filings",
        "impact": "high",
    },
    {
        "topic": "FSD take rate",
        "reason": "Conflicting reports (10-30%)",
        "impact": "high",
    },
    {
        "topic": "Cybertruck production costs",
        "reason": "Internal data only",
        "impact": "medium",
    },
]

MOCK_RECOMMENDATIONS = [
    {
        "priority": "urgent",
        "action": "Monitor Q1 2025 earnings call",
        "rationale": "Margin pressure from price cuts may impact profitability",
        "deadline": "April 2025",
    },
    {
        "priority": "strategic",
        "action": "Evaluate Model 2 timeline",
        "rationale": "Critical for mass market against BYD competition",
        "deadline": "Q2 2025",
    },
    {
        "priority": "monitor",
        "action": "Track BYD Europe expansion",
        "rationale": "Key competitive threat in European markets",
        "deadline": "Ongoing",
    },
]

MOCK_REPORT = """
## Executive Summary

Tesla maintains leadership in US EV market (55% share) but faces increasing pressure from BYD and Chinese competitors. Key strengths include vertical integration and Supercharger network, while challenges include quality control and margin pressure from price cuts.

**Recommendation:** Monitor Q1 2025 earnings for pricing strategy and Model 2 timeline.

---

## Key Metrics

| Metric | Value | Trend | Confidence |
|--------|-------|-------|------------|
| Revenue (2024) | $96.8B | ↗ +38% | <span class="badge badge-success"><span class="mdi mdi-shield-check"></span> High</span> |
| Market Cap | $850B | ↘ -15% YTD | <span class="badge badge-success"><span class="mdi mdi-shield-check"></span> High</span> |
| US EV Share | 55% | ↘ -10 pts | <span class="badge badge-warning"><span class="mdi mdi-shield-alert"></span> Medium</span> |
| Global Deliveries | 1.8M units | ↗ +38% | <span class="badge badge-success"><span class="mdi mdi-shield-check"></span> High</span> |

---

## Market Position Consensus

<div class="consensus-meter">
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="color: #a1a1aa;">Market Leader</span>
        <span style="color: #10b981; font-weight: 600;">85% sources agree</span>
    </div>
    <div class="consensus-bar">
        <div class="consensus-fill" style="width: 85%;"></div>
    </div>
    <p style="margin: 0.5rem 0 0; font-size: 0.85rem; color: #71717a;">
        17 of 20 sources identify Tesla as market leader in US EV segment
    </p>
</div>

---

## SWOT Analysis

**Strengths**
- Brand recognition and customer loyalty <span class="badge badge-success">High</span>
- Vertical integration (manufacturing to retail) <span class="badge badge-success">High</span>
- Supercharger network (55,000+ stalls) <span class="badge badge-success">High</span>
- Software/OTA update capability <span class="badge badge-success">High</span>

**Weaknesses**
- Quality control inconsistencies <span class="badge badge-warning">Medium</span>
- CEO-dependent brand perception <span class="badge badge-success">High</span>
- Limited model variety vs competitors <span class="badge badge-warning">Medium</span>

**Opportunities**
- FSD licensing revenue potential <span class="badge badge-warning">Medium</span>
- Energy storage market growth (25% CAGR) <span class="badge badge-success">High</span>
- Model 2 for mass market penetration <span class="badge badge-success">High</span>

**Threats**
- BYD and Chinese EV competition <span class="badge badge-success">High</span>
- Legacy automaker electrification push <span class="badge badge-success">High</span>
- Regulatory and trade policy changes <span class="badge badge-warning">Medium</span>
"""

# ─────────────────────────────────────────────────────────────────────────────
# Component Renderers
# ─────────────────────────────────────────────────────────────────────────────


def render_header() -> str:
    """Premium header (from am1 style)."""
    return f"""
    <link rel="stylesheet" href="{MDI_CDN}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <style>{THEME_CSS}</style>
    <div style="background: {COLORS["gradient_header"]}; padding: 1.5rem 2rem; border-bottom: 1px solid {COLORS["border"]};">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="background: {COLORS["gradient_accent"]}; width: 48px; height: 48px; 
                        border-radius: 12px; display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);">
                <span class="mdi mdi-chart-timeline-variant-shimmer" style="color: white; font-size: 1.5rem;"></span>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 1.5rem; color: {COLORS["text_primary"]};">Market Intelligence</h1>
                <p style="margin: 0.25rem 0 0; color: {COLORS["text_secondary"]}; font-size: 0.9rem;">
                    Enterprise-grade competitive research in minutes
                </p>
            </div>
        </div>
    </div>
    """


def render_research_types() -> str:
    """Research type cards (from am1, with better spacing)."""
    cards = ""
    for i, (name, icon, desc) in enumerate(RESEARCH_TYPES):
        active = "active" if i == 0 else ""
        cards += f"""
        <div class="research-card {active}" style="flex: 1; min-width: 180px;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <div style="background: {COLORS["accent_muted"]}; width: 36px; height: 36px; 
                            border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                    <span class="mdi mdi-{icon}" style="font-size: 1.25rem; color: {COLORS["accent"]};"></span>
                </div>
                <span style="font-weight: 600; color: {COLORS["text_primary"]};">{name}</span>
            </div>
            <p style="margin: 0; font-size: 0.8rem; color: {COLORS["text_muted"]}; line-height: 1.4;">{desc}</p>
        </div>
        """

    return f"""
    <div style="padding: 1.5rem 2rem;">
        <div class="section-header">
            <span class="mdi mdi-format-list-bulleted-type" style="color: {COLORS["accent"]};"></span>
            What do you need?
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            {cards}
        </div>
    </div>
    """


def render_progress() -> str:
    """Centered progress (from am2)."""
    return f"""
    <div style="padding: 1.5rem 2rem;">
        <div class="progress-container">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; justify-content: center;">
                <span class="mdi mdi-loading" style="color: {COLORS["accent"]}; font-size: 1.25rem; animation: pulse 1.5s infinite;"></span>
                <span style="color: {COLORS["text_secondary"]}; font-weight: 500;">Researching Tesla...</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 65%;"></div>
            </div>
            <p style="font-size: 0.85rem; color: {COLORS["text_muted"]}; margin-top: 0.75rem;">
                Gathering sources • Analyzing competitors • Generating report
            </p>
        </div>
    </div>
    """


def render_sources_tab() -> str:
    """Sources in tab (from am2, with am1 card style)."""
    cards = ""
    for source in MOCK_SOURCES:
        fresh_badge = (
            '<span class="badge badge-success"><span class="mdi mdi-check-circle"></span> Fresh</span>'
            if source["freshness"] == "fresh"
            else '<span class="badge badge-warning"><span class="mdi mdi-clock"></span> Recent</span>'
        )
        conf_badge = (
            f'<span class="badge badge-success"><span class="mdi mdi-shield-check"></span> {source["confidence"].title()}</span>'
            if source["confidence"] == "high"
            else f'<span class="badge badge-warning"><span class="mdi mdi-shield-alert"></span> {source["confidence"].title()}</span>'
        )

        cards += f"""
        <div class="source-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                <div>
                    <div style="font-weight: 600; color: {COLORS["text_primary"]}; margin-bottom: 0.25rem;">{source["title"]}</div>
                    <div style="font-size: 0.8rem; color: {COLORS["text_muted"]};">
                        <span class="mdi mdi-web"></span> {source["source"]} • {source["date"]}
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    {fresh_badge}
                    {conf_badge}
                </div>
            </div>
            <div style="background: {COLORS["bg_primary"]}; border-left: 3px solid {COLORS["accent"]}; 
                        padding: 0.75rem 1rem; border-radius: 0 8px 8px 0; font-size: 0.85rem; 
                        color: {COLORS["text_secondary"]}; font-style: italic;">
                "{source["snippet"]}"
            </div>
            <a href="#" style="display: inline-flex; align-items: center; gap: 0.25rem; margin-top: 0.75rem; 
                               font-size: 0.8rem; color: {COLORS["accent"]}; text-decoration: none;">
                <span class="mdi mdi-open-in-new"></span> View Source
            </a>
        </div>
        """

    return f"""
    <div style="padding: 0 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div class="section-header" style="margin-bottom: 0;">
                <span class="mdi mdi-text-box-multiple" style="color: {COLORS["accent"]};"></span>
                Sources ({len(MOCK_SOURCES)})
            </div>
            <button style="background: transparent; border: 1px dashed {COLORS["border"]}; color: {COLORS["text_muted"]}; 
                           padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer; font-size: 0.85rem;">
                <span class="mdi mdi-plus"></span> Add Source
            </button>
        </div>
        {cards}
    </div>
    """


def render_intelligence_gaps() -> str:
    """Intelligence gaps section."""
    gaps = ""
    for gap in MOCK_GAPS:
        impact_colors = {
            "high": COLORS["error"],
            "medium": COLORS["warning"],
            "low": COLORS["success"],
        }
        gaps += f"""
        <div style="padding: 0.75rem 0; border-bottom: 1px solid rgba(245, 158, 11, 0.2);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="font-weight: 600; color: {COLORS["warning"]};">{gap["topic"]}</span>
                <span style="font-size: 0.75rem; color: {impact_colors[gap["impact"]]};">
                    <span class="mdi mdi-alert-circle"></span> {gap["impact"].upper()} IMPACT
                </span>
            </div>
            <p style="margin: 0; font-size: 0.85rem; color: {COLORS["text_muted"]};">{gap["reason"]}</p>
        </div>
        """

    return f"""
    <div class="gaps-section" style="margin: 1.5rem 0;">
        <div class="section-header" style="color: {COLORS["warning"]};">
            <span class="mdi mdi-file-question"></span>
            What We Couldn't Find
        </div>
        {gaps}
    </div>
    """


def render_recommendations() -> str:
    """Actionable recommendations."""
    recs = ""
    priority_styles = {
        "urgent": (COLORS["error"], "mdi-alert-octagon", COLORS["error_bg"]),
        "strategic": (COLORS["info"], "mdi-chess-queen", COLORS["info_bg"]),
        "monitor": (COLORS["success"], "mdi-eye", COLORS["success_bg"]),
    }

    for i, rec in enumerate(MOCK_RECOMMENDATIONS, 1):
        color, icon, bg = priority_styles[rec["priority"]]
        recs += f"""
        <div class="card" style="margin-bottom: 1rem; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                <span class="badge" style="background: {bg}; color: {color};">
                    <span class="mdi {icon}"></span> {rec["priority"].upper()}
                </span>
                <span style="font-size: 0.8rem; color: {COLORS["text_muted"]};">
                    <span class="mdi mdi-calendar-clock"></span> {rec["deadline"]}
                </span>
            </div>
            <div style="font-weight: 600; color: {COLORS["text_primary"]}; margin-bottom: 0.5rem;">
                {i}. {rec["action"]}
            </div>
            <p style="margin: 0; font-size: 0.875rem; color: {COLORS["text_muted"]};">
                <strong style="color: {COLORS["text_secondary"]};">Rationale:</strong> {rec["rationale"]}
            </p>
        </div>
        """

    return f"""
    <div style="margin: 1.5rem 0;">
        <div class="section-header">
            <span class="mdi mdi-pin" style="color: {COLORS["accent"]};"></span>
            Recommended Actions
        </div>
        {recs}
    </div>
    """


def render_hitl_checkpoint() -> str:
    """HITL checkpoint (from am2, refined)."""
    return f"""
    <div class="hitl-checkpoint">
        <div class="section-header" style="color: {COLORS["accent"]}; margin-bottom: 0.75rem;">
            <span class="mdi mdi-account-check"></span>
            Human Review Checkpoint
        </div>
        <p style="color: {COLORS["text_secondary"]}; margin: 0 0 1.25rem 0; font-size: 0.9rem;">
            Review the analysis before finalizing. You can edit insights, add context, or request revisions.
        </p>
        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button class="export-btn" style="background: {COLORS["gradient_accent"]}; color: white;">
                <span class="mdi mdi-check"></span> Approve & Continue
            </button>
            <button class="export-btn export-copy">
                <span class="mdi mdi-pencil"></span> Request Revisions
            </button>
            <button class="export-btn export-copy">
                <span class="mdi mdi-download"></span> Download Draft
            </button>
        </div>
    </div>
    """


def render_export_buttons() -> str:
    """Export buttons (centered, with theme colors)."""
    return """
    <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; margin: 2rem 0;">
        <button class="export-btn export-pdf">
            <span class="mdi mdi-file-pdf-box"></span> Export PDF
        </button>
        <button class="export-btn export-csv">
            <span class="mdi mdi-file-delimited"></span> Export CSV
        </button>
        <button class="export-btn export-copy">
            <span class="mdi mdi-content-copy"></span> Copy Report
        </button>
        <button class="export-btn export-share">
            <span class="mdi mdi-share-variant"></span> Share
        </button>
        <button class="export-btn export-copy">
            <span class="mdi mdi-bookmark"></span> Save
        </button>
    </div>
    """


def render_footer() -> str:
    """Clean footer."""
    return f"""
    <div style="text-align: center; padding: 2rem; border-top: 1px solid {COLORS["border"]}; margin-top: 2rem;">
        <p style="margin: 0 0 0.5rem; color: {COLORS["text_secondary"]}; font-weight: 600;">
            Market Intelligence
        </p>
        <p style="margin: 0; font-size: 0.85rem; color: {COLORS["text_muted"]};">
            <span class="mdi mdi-graph" style="color: {COLORS["accent"]};"></span> LangGraph • 
            <span class="mdi mdi-api" style="color: {COLORS["accent"]};"></span> OpenRouter • 
            <span class="mdi mdi-magnify" style="color: {COLORS["accent"]};"></span> Tavily
        </p>
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────


def create_mock_ui() -> gr.Blocks:
    """Create best-of-both UI mock."""

    with gr.Blocks() as app:
        # Header (am1 style)
        gr.HTML(render_header())

        # Research Type Cards (am1 style, better spacing)
        gr.HTML(render_research_types())

        # Input Section
        with gr.Row():
            with gr.Column():
                gr.Textbox(
                    label="Company or Topic",
                    value="Tesla",
                    placeholder="Enter company name, market, or research topic...",
                )
                gr.Button("Generate Report", variant="primary", size="lg")

        # Progress (centered, am2 style)
        gr.HTML(render_progress())

        # Tabs (Report / Sources - from am2)
        with gr.Tabs():
            with gr.TabItem("Report"):
                gr.HTML(f"""
                <div style="padding: 0 2rem;">
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <div class="section-header" style="margin: 0;">
                                <span class="mdi mdi-file-document-outline" style="color: {COLORS["accent"]};"></span>
                                Analysis Report
                            </div>
                            <span class="badge badge-success">
                                <span class="mdi mdi-check-circle"></span> Complete
                            </span>
                        </div>
                    </div>
                </div>
                """)
                gr.Markdown(MOCK_REPORT, elem_classes=["report-content"])
                gr.HTML(
                    f"<div style='padding: 0 2rem;'>{render_intelligence_gaps()}</div>"
                )
                gr.HTML(
                    f"<div style='padding: 0 2rem;'>{render_recommendations()}</div>"
                )
                gr.HTML(
                    f"<div style='padding: 0 2rem;'>{render_hitl_checkpoint()}</div>"
                )

            with gr.TabItem("Sources"):
                gr.HTML(render_sources_tab())

        # Export Buttons (centered, with colors)
        gr.HTML(render_export_buttons())

        # Footer
        gr.HTML(render_footer())

    return app


if __name__ == "__main__":
    app = create_mock_ui()
    print("\n" + "=" * 70)
    print("  MARKET INTELLIGENCE UI MOCK v3")
    print("  Best of am1 + am2")
    print()
    print("  URL: http://127.0.0.1:7864")
    print("  Features: Cards | Tabs | Centered Progress | HITL | Export")
    print("=" * 70 + "\n")
    app.launch(server_name="127.0.0.1", server_port=7864, share=False)
