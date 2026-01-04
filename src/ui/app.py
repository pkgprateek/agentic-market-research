"""Market Intelligence UI — F2: Company Analysis.

Production UI with workflow integration.
Based on app_mock.py design, wired to MarketIntelligenceWorkflow.
"""

import asyncio
import os

import gradio as gr
import markdown  # type: ignore[import-untyped]

from src.workflows.market_analysis import MarketIntelligenceWorkflow
from src.workflows.types import ResearchType

# ─────────────────────────────────────────────────────────────────────────────
# Design System
# ─────────────────────────────────────────────────────────────────────────────

COLORS = {
    "bg_primary": "#0a0a0c",
    "bg_secondary": "#131316",
    "bg_elevated": "#1a1a1f",
    "bg_card": "#16161a",
    "border": "#2a2a33",
    "border_accent": "#3d3d4a",
    "text_primary": "#f4f4f5",
    "text_secondary": "#a1a1aa",
    "text_muted": "#71717a",
    "accent": "#14b8a6",
    "accent_hover": "#2dd4bf",
    "accent_muted": "rgba(20, 184, 166, 0.15)",
    "success": "#10b981",
    "success_bg": "rgba(16, 185, 129, 0.15)",
    "warning": "#f59e0b",
    "warning_bg": "rgba(245, 158, 11, 0.15)",
    "error": "#ef4444",
    "error_bg": "rgba(239, 68, 68, 0.15)",
    "info": "#3b82f6",
    "info_bg": "rgba(59, 130, 246, 0.15)",
}

MDI_CDN = "https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css"

# Container for consistent spacing
CONTAINER = "max-width: 900px; margin: 0 auto; padding: 0 1.5rem;"

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────

THEME_CSS = f"""
* {{ box-sizing: border-box; }}

.gradio-container {{
    background: {COLORS["bg_secondary"]} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {COLORS["text_primary"]} !important;
    padding: 0 !important;
    margin: 0 !important;
}}

.dark, .gr-form, .gr-box, .gr-panel {{
    background: {COLORS["bg_primary"]} !important;
}}

h1, h2, h3, h4 {{
    color: {COLORS["text_primary"]} !important;
    font-weight: 600 !important;
}}

/* Buttons */
button.primary {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, #0d9488 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3) !important;
}}

/* Small buttons */
.btn-sm {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    height: 36px;
    padding: 0 0.875rem;
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    color: {COLORS["text_muted"]};
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
}}

.btn-sm:hover {{
    border-color: {COLORS["accent"]};
    color: {COLORS["text_primary"]};
}}

/* Research Type Cards with shadow (like am1) */
.research-card {{
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}}

.research-card:hover {{
    border-color: {COLORS["accent"]};
    background: {COLORS["bg_elevated"]};
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}}

.research-card.active {{
    border-color: {COLORS["accent"]};
    background: {COLORS["accent_muted"]};
    box-shadow: 0 0 0 3px {COLORS["accent_muted"]}, 0 8px 24px rgba(20, 184, 166, 0.2);
}}

.research-card-icon {{
    width: 36px;
    height: 36px;
    min-width: 36px;
    background: {COLORS["accent_muted"]};
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.research-card-icon .mdi {{
    font-size: 1.25rem;
    color: {COLORS["accent"]};
}}

.research-card-title {{
    font-weight: 600;
    font-size: 0.9rem;
    color: {COLORS["text_primary"]};
    margin-bottom: 0.125rem;
}}

.research-card-desc {{
    font-size: 0.75rem;
    color: {COLORS["text_muted"]};
    line-height: 1.3;
}}

/* Cards */
.card {{
    background: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 1.25rem;
}}

/* Source Card */
.source-card {{
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 1rem;
    margin: 0.75rem 0;
}}

/* Progress */
.progress-bar {{
    height: 4px;
    background: {COLORS["border"]};
    border-radius: 2px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, {COLORS["accent"]}, {COLORS["accent_hover"]});
}}

/* Consensus */
.consensus-bar {{
    height: 8px;
    background: {COLORS["border"]};
    border-radius: 4px;
    overflow: hidden;
}}

.consensus-fill {{
    height: 100%;
    background: linear-gradient(90deg, {COLORS["success"]}, #059669);
}}

/* Badges */
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.6rem;
    border-radius: 5px;
    font-size: 0.7rem;
    font-weight: 600;
}}

.badge-success {{ background: {COLORS["success_bg"]}; color: {COLORS["success"]}; }}
.badge-warning {{ background: {COLORS["warning_bg"]}; color: {COLORS["warning"]}; }}
.badge-error {{ background: {COLORS["error_bg"]}; color: {COLORS["error"]}; }}
.badge-info {{ background: {COLORS["info_bg"]}; color: {COLORS["info"]}; }}

/* HITL */
.hitl-box {{
    background: {COLORS["accent_muted"]};
    border: 2px solid {COLORS["accent"]};
    border-radius: 12px;
    padding: 1.25rem;
    margin: 2rem 0;
}}

/* Export buttons */
.export-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    height: 40px;
    padding: 0 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: all 0.15s;
}}

.export-btn:hover {{
    transform: translateY(-1px);
}}

/* Gaps */
.gaps-box {{
    background: {COLORS["warning_bg"]};
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 10px;
    padding: 1rem;
    border-top: 3px solid {COLORS["warning"]};
    margin: 1.5rem 0;
}}

/* Report container */
.report-wrapper {{
    {CONTAINER}
}}

.report-box {{
    background: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 1.5rem;
}}

/* Report content - professional typography */
.report-md h2 {{
    color: {COLORS["text_primary"]};
    font-size: 1.25rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {COLORS["border"]};
    letter-spacing: -0.01em;
}}

.report-md h3 {{
    color: {COLORS["text_primary"]};
    font-size: 1rem;
    font-weight: 600;
    margin: 1.5rem 0 0.75rem 0;
}}

.report-md p {{
    color: {COLORS["text_secondary"]};
    font-size: 0.9rem;
    line-height: 1.7;
    margin: 0.75rem 0;
}}

.report-md strong {{
    color: {COLORS["text_primary"]};
    font-weight: 600;
}}

.report-md ul, .report-md ol {{
    color: {COLORS["text_secondary"]};
    font-size: 0.9rem;
    line-height: 1.7;
    padding-left: 1.5rem;
    margin: 0.75rem 0;
}}

.report-md li {{
    margin: 0.35rem 0;
}}

.report-md hr {{
    border: none;
    border-top: 1px solid {COLORS["border"]};
    margin: 1.5rem 0;
}}

.report-md table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.85rem;
}}

.report-md th, .report-md td {{
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid {COLORS["border"]};
}}

.report-md th {{
    background: {COLORS["bg_elevated"]};
    color: {COLORS["text_muted"]};
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.report-md td {{
    color: {COLORS["text_secondary"]};
}}

/* Focus Areas - uses details/summary for native collapse */
.focus-areas {{
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
    margin-top: 1rem;
}}

.focus-areas summary {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    cursor: pointer;
    list-style: none;
}}

.focus-areas summary::-webkit-details-marker {{
    display: none;
}}

.focus-areas summary:hover {{
    background: {COLORS["bg_elevated"]};
    border-radius: 10px;
}}

.focus-areas[open] summary {{
    border-bottom: 1px solid {COLORS["border"]};
    border-radius: 10px 10px 0 0;
}}

.focus-checkbox {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
}}

.focus-checkbox:hover {{
    background: {COLORS["bg_elevated"]};
}}

.focus-checkbox input {{
    width: 16px;
    height: 16px;
    accent-color: {COLORS["accent"]};
}}

/* Tabs alignment - wrap content in container */
.tabs {{
    {CONTAINER}
}}

.tabitem {{
    padding: 0 !important;
}}

/* Tab styling - active state visibility */
.tab-nav {{
    border-bottom: 1px solid {COLORS["border"]} !important;
    margin-bottom: 1.5rem !important;
}}

.tab-nav button {{
    background: transparent !important;
    border: none !important;
    color: {COLORS["text_muted"]} !important;
    padding: 0.75rem 1rem !important;
    font-weight: 500 !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s !important;
}}

.tab-nav button:hover {{
    color: {COLORS["text_primary"]} !important;
    background: {COLORS["bg_secondary"]} !important;
}}

.tab-nav button.selected {{
    color: {COLORS["accent"]} !important;
    background: {COLORS["accent_muted"]} !important;
    border-bottom: 2px solid {COLORS["accent"]} !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {COLORS["bg_primary"]}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS["border"]}; border-radius: 4px; }}

/* Gradio Component Overrides - aggressive selectors for Gradio 6.x */
input[type="text"], input[type="search"], textarea {{
    background: {COLORS["bg_secondary"]} !important;
    border: 1px solid {COLORS["border"]} !important;
    border-radius: 10px !important;
    color: {COLORS["text_primary"]} !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    height: 48px !important;
    width: 100% !important;
}}

input[type="text"]:focus, input[type="search"]:focus, textarea:focus {{
    border-color: {COLORS["accent"]} !important;
    outline: none !important;
    box-shadow: 0 0 0 2px {COLORS["accent_muted"]} !important;
}}

input::placeholder, textarea::placeholder {{
    color: {COLORS["text_muted"]} !important;
}}

/* Gradio button - target all primary buttons */
button[class*="primary"], button.lg {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, #0d9488 100%) !important;
    border: none !important;
    height: 48px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3) !important;
    width: 100% !important;
}}

button[class*="primary"]:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(20, 184, 166, 0.4) !important;
}}

/* Row layout for inputs */
.gr-row {{
    gap: 0.75rem !important;
}}

/* Animations */
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Mock Data
# ─────────────────────────────────────────────────────────────────────────────

RESEARCH_TYPES = [
    ("Company Analysis", "domain", "Deep dive on a single company"),
    ("Competitive Comparison", "compare", "Compare 2-5 companies"),
    ("Market Landscape", "earth", "Market overview & trends"),
    ("Battle Card", "sword-cross", "Sales enablement"),
    ("Investment Thesis", "cash-multiple", "Due diligence report"),
    ("Custom Query", "help-circle", "Free-form research"),
]

# From CLAUDE.md F2
FOCUS_AREAS = [
    ("Products & Services", "Product offerings, features, and service portfolio", True),
    ("Pricing", "Pricing models, tiers, and competitive positioning", False),
    ("Leadership", "Executive team, board, and organizational structure", False),
    ("Financials", "Revenue, margins, funding, and financial health", True),
    ("Market Position", "Market share, competitive landscape, and positioning", True),
]

MOCK_SOURCES = [
    {
        "title": "Tesla Q4 2024 Earnings Report",
        "source": "Tesla IR",
        "date": "Jan 2025",
        "freshness": "fresh",
        "confidence": "high",
        "snippet": "Tesla delivered 1.8M vehicles in 2024, up 38% YoY.",
        "description": "Official quarterly earnings release with financial metrics and delivery numbers",
    },
    {
        "title": "Global EV Market Analysis",
        "source": "BloombergNEF",
        "date": "Dec 2024",
        "freshness": "fresh",
        "confidence": "high",
        "snippet": "Global EV sales reached 14.1M units in 2024.",
        "description": "Comprehensive market analysis covering global EV adoption trends",
    },
    {
        "title": "Tesla vs BYD Competition",
        "source": "Reuters",
        "date": "Dec 2024",
        "freshness": "fresh",
        "confidence": "medium",
        "snippet": "BYD overtook Tesla in quarterly deliveries for the first time.",
        "description": "Competitive analysis comparing delivery numbers and market positioning",
    },
]

MOCK_REPORT = """
## Executive Summary

Tesla maintains leadership in US EV market (55% share) but faces increasing pressure from BYD and Chinese competitors.

**Recommendation:** Monitor Q1 2025 earnings for pricing strategy and Model 2 timeline.

---

## Key Metrics

| Metric | Value | Trend | Confidence |
|--------|-------|-------|------------|
| Revenue (2024) | $96.8B | ↗ +38% | <span class="badge badge-success">High</span> |
| Market Cap | $850B | ↘ -15% YTD | <span class="badge badge-success">High</span> |
| US EV Share | 55% | ↘ -10 pts | <span class="badge badge-warning">Medium</span> |

---

## Market Position Consensus

<div style="background: #0a0a0c; border: 1px solid #2a2a33; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="color: #a1a1aa;">Market Leader</span>
        <span style="color: #10b981; font-weight: 600;">85% sources agree</span>
    </div>
    <div class="consensus-bar">
        <div class="consensus-fill" style="width: 85%;"></div>
    </div>
</div>

---

## SWOT Analysis

**Strengths**
- Brand recognition and customer loyalty <span class="badge badge-success">High</span>
- Vertical integration <span class="badge badge-success">High</span>
- Supercharger network (55,000+ stalls) <span class="badge badge-success">High</span>

**Weaknesses**
- Quality control inconsistencies <span class="badge badge-warning">Medium</span>

**Opportunities**
- FSD licensing revenue potential <span class="badge badge-warning">Medium</span>

**Threats**
- BYD and Chinese EV competition <span class="badge badge-success">High</span>
"""

# ─────────────────────────────────────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────────────────────────────────────


def render_base() -> str:
    """Base styles."""
    return f"""
    <link rel="stylesheet" href="{MDI_CDN}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <style>{THEME_CSS}</style>
    """


def render_header() -> str:
    """Header with transparent background - gradient comes from page."""
    return f"""
    <div style="background: transparent;
                padding: 1.25rem 0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
        <div style="{CONTAINER}">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="background: linear-gradient(135deg, {COLORS["accent"]}, #0d9488);
                            width: 44px; height: 44px; border-radius: 12px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.4);">
                    <span class="mdi mdi-chart-timeline-variant-shimmer" style="color: white; font-size: 1.5rem;"></span>
                </div>
                <div>
                    <h1 style="margin: 0; font-size: 1.35rem; color: {COLORS["text_primary"]}; font-weight: 700;">
                        Market Intelligence
                    </h1>
                    <p style="margin: 0; font-size: 0.8rem; color: {COLORS["text_muted"]};">
                        Enterprise-grade competitive research
                    </p>
                </div>
            </div>
        </div>
    </div>
    """


def render_research_types() -> str:
    """Research type cards (3x2 grid with shadows)."""
    cards = ""
    for i, (name, icon, desc) in enumerate(RESEARCH_TYPES):
        active = "active" if i == 0 else ""
        cards += f"""
        <div class="research-card {active}">
            <div class="research-card-icon">
                <span class="mdi mdi-{icon}"></span>
            </div>
            <div>
                <div class="research-card-title">{name}</div>
                <div class="research-card-desc">{desc}</div>
            </div>
        </div>
        """

    return f"""
    <div style="padding: 1.5rem 0;">
        <div style="{CONTAINER}">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span class="mdi mdi-format-list-bulleted-type" style="color: {COLORS["accent"]}; font-size: 1.25rem;"></span>
                <span style="font-weight: 600; color: {COLORS["text_primary"]};">What do you need?</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem;">
                {cards}
            </div>
        </div>
    </div>
    """


def render_input_section() -> str:
    """Input with Focus Areas accordion."""
    # Build focus area checkboxes
    focus_items = ""
    for name, desc, checked in FOCUS_AREAS:
        checked_attr = "checked" if checked else ""
        focus_items += f"""
        <label class="focus-checkbox">
            <input type="checkbox" {checked_attr}>
            <div>
                <div style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.9rem;">{name}</div>
                <div style="font-size: 0.75rem; color: {COLORS["text_muted"]};">{desc}</div>
            </div>
        </label>
        """

    return f"""
    <div style="padding: 0 0 1.5rem;">
        <div style="{CONTAINER}">
            <!-- Company Input -->
            <div style="margin-bottom: 1rem;">
                <label style="display: block; margin-bottom: 0.5rem; font-size: 0.85rem; color: {COLORS["text_secondary"]}; font-weight: 500;">
                    Company Name
                </label>
                <div style="position: relative;">
                    <input type="text" value="Tesla" placeholder="Enter company name..."
                           style="width: 100%; height: 48px; padding: 0 1rem 0 2.75rem; font-size: 1rem;
                                  background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]};
                                  border-radius: 10px; color: {COLORS["text_primary"]};">
                    <span class="mdi mdi-magnify" style="position: absolute; left: 1rem; top: 50%;
                          transform: translateY(-50%); color: {COLORS["text_muted"]}; font-size: 1.25rem;"></span>
                </div>
            </div>

            <!-- Focus Areas Accordion (collapsed by default) -->
            <details class="focus-areas">
                <summary>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="mdi mdi-tune" style="color: {COLORS["accent"]};"></span>
                        <span style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.9rem;">Focus Areas</span>
                        <span style="font-size: 0.75rem; color: {COLORS["text_muted"]};">({sum(1 for _, _, c in FOCUS_AREAS if c)} selected)</span>
                    </div>
                    <span class="mdi mdi-chevron-down" style="color: {COLORS["text_muted"]};"></span>
                </summary>
                <div style="padding: 0.5rem 0;">
                    {focus_items}
                </div>
            </details>

            <!-- Advanced Settings Button -->
            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                <button class="btn-sm"><span class="mdi mdi-cog"></span> Advanced Settings</button>
            </div>

            <!-- Generate Button -->
            <button style="width: 100%; height: 48px; margin-top: 1rem;
                           background: linear-gradient(135deg, {COLORS["accent"]}, #0d9488);
                           border: none; border-radius: 10px; color: white; font-weight: 600; font-size: 1rem;
                           cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem;
                           box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3); transition: all 0.2s;">
                <span class="mdi mdi-play"></span> Generate Report
            </button>
        </div>
    </div>
    """


def render_progress() -> str:
    """Progress bar."""
    return f"""
    <div style="padding: 0 0 0.8rem;">
        <div style="{CONTAINER}">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span class="mdi mdi-loading" style="color: {COLORS["accent"]}; font-size: 1rem; animation: spin 1s linear infinite;"></span>
                <span style="color: {COLORS["text_secondary"]}; font-size: 0.9rem;">Researching Tesla...</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 65%;"></div>
            </div>
            <p style="margin: 0.5rem 0 0; font-size: 0.8rem; color: {COLORS["text_muted"]};">
                Gathering sources • Analyzing competitors • Generating report
            </p>
        </div>
    </div>
    """


def render_report_header() -> str:
    """Report header inside container."""
    return f"""
    <div style="{CONTAINER}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["text_primary"]}; display: flex; align-items: center; gap: 0.5rem;">
                <span class="mdi mdi-file-document-outline" style="color: {COLORS["accent"]};"></span>
                Analysis Report
            </h3>
            <span class="badge badge-success"><span class="mdi mdi-check-circle"></span> Complete</span>
        </div>
    </div>
    """


def render_gaps() -> str:
    """Intelligence gaps - compact layout."""
    gaps = [
        (
            "Exact gross margin by product line",
            "Not disclosed in public filings",
            "HIGH",
        ),
        ("FSD take rate", "Conflicting reports (10-30%)", "HIGH"),
    ]

    items = ""
    for topic, reason, impact in gaps:
        color = COLORS["error"] if impact == "HIGH" else COLORS["warning"]
        items += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.5rem 0; border-bottom: 1px solid rgba(245, 158, 11, 0.15);">
            <div style="flex: 1; min-width: 0;">
                <span style="font-weight: 600; color: {COLORS["text_primary"]}; font-size: 0.85rem;">{topic}</span>
                <p style="margin: 0.25rem 0 0; font-size: 0.75rem; color: {COLORS["text_muted"]}; line-height: 1.3;">{reason}</p>
            </div>
            <span style="font-size: 0.65rem; color: {color}; font-weight: 600; white-space: nowrap;">{impact}</span>
        </div>
        """

    return f"""
    <div class="gaps-box">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span class="mdi mdi-file-question" style="color: {COLORS["warning"]}; font-size: 1.1rem;"></span>
            <h3 style="margin: 0; font-size: 0.9rem; color: {COLORS["warning"]};">What We Couldn't Find</h3>
        </div>
        {items}
    </div>
    """


def render_recommendations() -> str:
    """Recommendations - compact layout similar to sources."""
    recs = [
        (
            "URGENT",
            "error",
            "mdi-alert-octagon",
            "Monitor Q1 2025 earnings call",
            "Apr 2025",
            "Review pricing strategy and Model 2 announcement timing",
        ),
        (
            "STRATEGIC",
            "info",
            "mdi-chess-queen",
            "Evaluate Model 2 timeline",
            "Q2 2025",
            "Assess competitive positioning and market entry strategy",
        ),
    ]

    items = ""
    for priority, color_key, icon, action, deadline, description in recs:
        bg = COLORS[f"{color_key}_bg"]
        color = COLORS[color_key]
        items += f"""
        <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem; margin-bottom: 0.5rem;
                    background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]};
                    border-left: 3px solid {color}; border-radius: 8px;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 0.15rem; min-width: 24px;">
                <span class="mdi mdi-pin" style="color: {COLORS["accent"]}; font-size: 0.9rem;"></span>
            </div>
            <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.85rem;">{action}</div>
                <div style="font-size: 0.75rem; color: {COLORS["text_muted"]}; margin-top: 0.25rem; line-height: 1.4;">
                    {description}
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem; padding-left: 0.5rem; min-width: 100px;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 0.7rem; color: {COLORS["text_muted"]}; font-weight: 500;">
                        <span class="mdi mdi-calendar-clock" style="font-size: 0.75rem;"></span> {deadline}
                    </span>
                </div>
                <span class="badge" style="background: {bg}; color: {color}; font-size: 0.65rem; padding: 0.15rem 0.4rem;">
                    <span class="mdi {icon}" style="font-size: 0.7rem;"></span> {priority}
                </span>
            </div>
        </div>
        """

    return f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span class="mdi mdi-pin" style="color: {COLORS["accent"]}; font-size: 1.1rem;"></span>
            <h3 style="margin: 0; font-size: 0.9rem; color: {COLORS["text_primary"]};">Recommended Actions</h3>
        </div>
        {items}
    </div>
    """


def render_hitl() -> str:
    """HITL checkpoint - compact layout."""
    return f"""
    <div class="hitl-box">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span class="mdi mdi-account-check" style="color: {COLORS["accent"]}; font-size: 1.1rem;"></span>
            <h3 style="margin: 0; font-size: 0.9rem; color: {COLORS["text_primary"]};">Human Review Checkpoint</h3>
        </div>
        <p style="margin: 0 0 0.75rem; color: {COLORS["text_secondary"]}; font-size: 0.85rem;">
            Review the analysis before finalizing.
        </p>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button class="export-btn" style="background: linear-gradient(135deg, {COLORS["success"]}, #059669); color: white;">
                <span class="mdi mdi-check"></span> Approve & Continue
            </button>
            <button class="export-btn" style="background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]};">
                <span class="mdi mdi-pencil"></span> Request Revisions
            </button>
        </div>
    </div>
    """


def render_export() -> str:
    """Export buttons - dark theme compatible."""
    return f"""
    <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; padding: 1.5rem 0;">
        <button class="export-btn" style="background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]};">
            <span class="mdi mdi-file-pdf-box" style="color: {COLORS["error"]};"></span> Export PDF
        </button>
        <button class="export-btn" style="background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]};">
            <span class="mdi mdi-file-delimited" style="color: {COLORS["success"]};"></span> Export CSV
        </button>
        <button class="export-btn" style="background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]};">
            <span class="mdi mdi-content-copy"></span> Copy
        </button>
        <button class="export-btn" style="background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]};">
            <span class="mdi mdi-share-variant" style="color: {COLORS["info"]};"></span> Share
        </button>
    </div>
    """


def render_full_report() -> str:
    """Render the complete report inside a single card container.

    Converts markdown to HTML so Executive Summary stays inside the card.
    """
    import markdown

    # Convert markdown to HTML with table support
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    report_html = md.convert(MOCK_REPORT)

    return f"""
    <div class="report-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid {COLORS["border"]};">
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["text_primary"]}; display: flex; align-items: center; gap: 0.5rem;">
                <span class="mdi mdi-file-document-outline" style="color: {COLORS["accent"]};"></span>
                Analysis Report
            </h3>
            <span class="badge badge-success"><span class="mdi mdi-check-circle"></span> Complete</span>
        </div>
        <div class="report-md">
            {report_html}
        </div>
    </div>
    """


def render_sources() -> str:
    """Sources tab - organized list with search/filter for scalability."""
    cards = ""
    for s in MOCK_SOURCES:
        conf_key = "success" if s["confidence"] == "high" else "warning"
        conf_color = COLORS[conf_key]
        conf_bg = COLORS[f"{conf_key}_bg"]
        conf_label = "High" if s["confidence"] == "high" else "Medium"
        freshness_icon = "mdi-check" if s["freshness"] == "fresh" else "mdi-alert"

        cards += f"""
        <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem;
                    border-bottom: 1px solid {COLORS["border"]}; transition: background 0.15s;"
                    onmouseover="this.style.background='{COLORS["bg_elevated"]}'"
                    onmouseout="this.style.background='transparent'">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 0.15rem; min-width: 24px;">
                <span class="mdi mdi-file-document-outline" style="color: {COLORS["accent"]}; font-size: 0.9rem;"></span>
                <span class="mdi {freshness_icon}" style="color: {conf_color}; font-size: 0.65rem;"></span>
            </div>
            <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.85rem;
                            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{s["title"]}</div>
                <div style="font-size: 0.75rem; color: {COLORS["text_muted"]}; margin-top: 0.25rem; line-height: 1.4;">
                    {s.get("description", "Source description placeholder")}
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem; padding-left: 0.5rem; min-width: 100px;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 0.7rem; color: {COLORS["text_muted"]};">{s["source"]}</span>
                    <span style="font-size: 0.65rem; color: {COLORS["border"]};">•</span>
                    <span style="font-size: 0.7rem; color: {COLORS["text_muted"]};">{s["date"]}</span>
                </div>
                <span style="font-size: 0.65rem; font-weight: 600; color: {conf_color}; background: {conf_bg};
                           padding: 0.15rem 0.4rem; border-radius: 4px;">{conf_label}</span>
            </div>
        </div>
        """

    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <h3 style="margin: 0; font-size: 0.95rem; color: {COLORS["text_primary"]}; display: flex; align-items: center; gap: 0.5rem;">
            <span class="mdi mdi-text-box-multiple" style="color: {COLORS["accent"]};"></span>
            Sources ({len(MOCK_SOURCES)})
        </h3>
        <div style="display: flex; gap: 0.5rem;">
            <button style="background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]};
                           color: {COLORS["text_muted"]}; font-size: 0.75rem; padding: 0.35rem 0.6rem;
                           border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 0.35rem;">
                <span class="mdi mdi-magnify" style="font-size: 0.8rem;"></span> Search
            </button>
            <button style="background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]};
                           color: {COLORS["text_muted"]}; font-size: 0.75rem; padding: 0.35rem 0.6rem;
                           border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 0.35rem;">
                <span class="mdi mdi-filter" style="font-size: 0.8rem;"></span> Filter
            </button>
        </div>
    </div>
    <div style="background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]}; border-radius: 10px;
                overflow-y: auto; max-height: 500px;">
        {cards}
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; padding: 0.5rem 0;">
        <span style="font-size: 0.75rem; color: {COLORS["text_muted"]};">Showing {len(MOCK_SOURCES)} sources</span>
        <div style="display: flex; gap: 0.35rem;">
            <button style="background: transparent; border: 1px solid {COLORS["border"]};
                           color: {COLORS["text_muted"]}; font-size: 0.7rem; padding: 0.25rem 0.5rem;
                           border-radius: 4px; cursor: pointer;">Previous</button>
            <button style="background: transparent; border: 1px solid {COLORS["border"]};
                           color: {COLORS["text_muted"]}; font-size: 0.7rem; padding: 0.25rem 0.5rem;
                           border-radius: 4px; cursor: pointer;">Next</button>
        </div>
    </div>
    """


def render_footer() -> str:
    """Footer."""
    return f"""
    <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid {COLORS["border"]}; margin-top: 1rem;">
        <p style="margin: 0; font-size: 0.85rem; color: {COLORS["text_muted"]};">
            <span class="mdi mdi-graph" style="color: {COLORS["accent"]};"></span> LangGraph •
            <span class="mdi mdi-api" style="color: {COLORS["accent"]};"></span> Groq •
            <span class="mdi mdi-magnify" style="color: {COLORS["accent"]};"></span> Tavily
        </p>
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
# Workflow Integration
# ─────────────────────────────────────────────────────────────────────────────


async def run_analysis_async(company_name: str, industry: str | None) -> tuple[str, list]:
    """Run the market intelligence workflow."""
    workflow = MarketIntelligenceWorkflow(checkpoint_path=":memory:")
    result = await workflow.run(
        company_name=company_name.strip(),
        industry=industry.strip() if industry else None,
        research_type=ResearchType.COMPANY_ANALYSIS,
    )
    return result.get("full_report", ""), result.get("raw_sources", [])


def generate_report(company_name: str, industry: str) -> tuple[str, str]:
    """Generate report and sources HTML."""
    if not company_name or not company_name.strip():
        return "<p style='color: #71717a;'>Enter a company name to generate a report.</p>", ""

    try:
        report_md, sources = asyncio.run(run_analysis_async(company_name, industry))

        # Convert markdown to HTML
        md = markdown.Markdown(extensions=["tables", "fenced_code"])
        report_html = f"<div class='report-md'>{md.convert(report_md)}</div>"

        # Format sources
        src_cards = ""
        for s in sources[:10]:
            title = s.get("title", "Untitled")[:60]
            content = (s.get("content", "")[:100] + "...") if s.get("content") else ""
            src_cards += f"""
            <div style="padding: 0.75rem; border-bottom: 1px solid #2a2a33;">
                <div style="font-weight: 500; color: #f4f4f5; font-size: 0.85rem;">{title}</div>
                <div style="font-size: 0.75rem; color: #71717a; margin-top: 0.25rem;">{content}</div>
            </div>"""

        sources_html = f"<div style='background: #131316; border-radius: 10px;'>{src_cards}</div>"
        return report_html, sources_html

    except Exception as e:
        return f"<p style='color: #ef4444;'>Error: {str(e)}</p>", ""


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────


def create_ui() -> gr.Blocks:
    """Create production UI with workflow integration."""

    with gr.Blocks() as app:
        # Base styles
        gr.HTML(render_base())

        # Header
        gr.HTML(render_header())

        # Research Types
        gr.HTML(render_research_types())

        # Input Section with Gradio components
        gr.HTML(f"""
        <div style="padding: 0 0 0.5rem;">
            <div style="{CONTAINER}">
                <label style="display: block; margin-bottom: 0.5rem; font-size: 0.85rem; color: {COLORS["text_secondary"]}; font-weight: 500;">
                    Company Name
                </label>
            </div>
        </div>
        """)

        # Wrap inputs in container for proper width
        gr.HTML(f"<div style='{CONTAINER}'>")
        with gr.Row():
            company_input = gr.Textbox(
                placeholder="Enter company name (e.g., Tesla, Apple)...",
                show_label=False,
                container=False,
                elem_classes=["gradio-textbox"],
            )
            industry_input = gr.Textbox(
                placeholder="Industry (optional)",
                show_label=False,
                container=False,
                elem_classes=["gradio-textbox"],
            )
        gr.HTML("</div>")

        # Focus Areas (static for now, can be wired later)
        gr.HTML(render_input_section_focus_only())

        # Generate button in container
        gr.HTML(f"<div style='{CONTAINER}'>")
        generate_btn = gr.Button(
            "Generate Report", variant="primary", size="lg", elem_classes=["gradio-button"]
        )
        gr.HTML("</div>")

        # Spacer
        gr.HTML("<div style='padding: 0.5rem 0;'></div>")

        # Report Tabs
        gr.HTML(f"<div style='{CONTAINER}'>")
        with gr.Tabs():
            with gr.TabItem("Report"):
                report_output = gr.HTML(
                    "<p style='color: #71717a; text-align: center; padding: 2rem;'>Enter a company name and click Generate Report.</p>"
                )

            with gr.TabItem("Sources"):
                sources_output = gr.HTML(
                    "<p style='color: #71717a; text-align: center; padding: 2rem;'>Sources will appear here after generating a report.</p>"
                )
        gr.HTML("</div>")

        # Wire button
        generate_btn.click(
            fn=generate_report,
            inputs=[company_input, industry_input],
            outputs=[report_output, sources_output],
        )

        # Footer
        gr.HTML(render_footer())

    return app


def render_input_section_focus_only() -> str:
    """Focus Areas accordion only (no company input, that's Gradio)."""
    focus_items = ""
    for name, desc, checked in FOCUS_AREAS:
        checked_attr = "checked" if checked else ""
        focus_items += f"""
        <label class="focus-checkbox">
            <input type="checkbox" {checked_attr}>
            <div>
                <div style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.9rem;">{name}</div>
                <div style="font-size: 0.75rem; color: {COLORS["text_muted"]};">{desc}</div>
            </div>
        </label>
        """

    return f"""
    <div style="padding: 0 0 1rem;">
        <div style="{CONTAINER}">
            <details class="focus-areas">
                <summary>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="mdi mdi-tune" style="color: {COLORS["accent"]};"></span>
                        <span style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.9rem;">Focus Areas</span>
                        <span style="font-size: 0.75rem; color: {COLORS["text_muted"]};">(3 selected)</span>
                    </div>
                    <span class="mdi mdi-chevron-down" style="color: {COLORS["text_muted"]};"></span>
                </summary>
                <div style="padding: 0.5rem 0;">
                    {focus_items}
                </div>
            </details>
        </div>
    </div>
    """


if __name__ == "__main__":
    is_deployment = os.getenv("SPACE_ID") or os.getenv("IS_DOCKER")
    server_name = "0.0.0.0" if is_deployment else "127.0.0.1"

    print("\n" + "=" * 60)
    print("  MARKET INTELLIGENCE — F2: Company Analysis")
    print(f"  URL: http://{server_name}:7860")
    print("=" * 60 + "\n")

    app = create_ui()
    app.launch(server_name=server_name, server_port=7860, share=False, show_error=True)
