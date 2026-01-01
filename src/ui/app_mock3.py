"""Enterprise-Grade UI Mock v3 — Best of Both Designs.

Fixes in this version:
1. Added shadows/effects to header and research cards (like am1)
2. Removed History button (not in CLAUDE.md)
3. Added "Generate Report" button
4. Added Focus Areas accordion from CLAUDE.md F2
5. Fixed report container alignment
6. Fixed tabs alignment with rest of app

Run: python -m src.ui.app_mock3
Port: 7864
"""

import gradio as gr

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

MDI_CDN = (
    "https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css"
)

# Container for consistent spacing
CONTAINER = "max-width: 900px; margin: 0 auto; padding: 0 1.5rem;"

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────

THEME_CSS = f"""
* {{ box-sizing: border-box; }}

.gradio-container {{
    background: {COLORS["bg_primary"]} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {COLORS["text_primary"]} !important;
    padding: 0 !important;
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
    padding: 1.5rem;
    margin: 1.5rem 0;
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
    padding: 1.25rem;
    border-top: 3px solid {COLORS["warning"]};
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

/* Report content */
.report-md h2 {{
    color: {COLORS["text_primary"]};
    margin-top: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {COLORS["border"]};
}}

.report-md table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}}

.report-md th, .report-md td {{
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid {COLORS["border"]};
}}

.report-md th {{
    background: {COLORS["bg_elevated"]};
    color: {COLORS["text_muted"]};
    font-size: 0.8rem;
    text-transform: uppercase;
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

/* Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {COLORS["bg_primary"]}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS["border"]}; border-radius: 4px; }}

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
    },
    {
        "title": "Global EV Market Analysis",
        "source": "BloombergNEF",
        "date": "Dec 2024",
        "freshness": "fresh",
        "confidence": "high",
        "snippet": "Global EV sales reached 14.1M units in 2024.",
    },
    {
        "title": "Tesla vs BYD Competition",
        "source": "Reuters",
        "date": "Dec 2024",
        "freshness": "fresh",
        "confidence": "medium",
        "snippet": "BYD overtook Tesla in quarterly deliveries for the first time.",
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
    """Header with shadow effect like am1."""
    return f"""
    <div style="background: linear-gradient(180deg, {COLORS["bg_secondary"]} 0%, {COLORS["bg_primary"]} 100%); 
                padding: 1.25rem 0; border-bottom: 1px solid {COLORS["border"]};
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
    <div style="padding: 0 0 1.5rem;">
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
    """Intelligence gaps."""
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
        <div style="padding: 0.75rem 0; border-bottom: 1px solid rgba(245, 158, 11, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span style="font-weight: 600; color: {COLORS["warning"]};">{topic}</span>
                <span style="font-size: 0.7rem; color: {color}; font-weight: 600;">{impact} IMPACT</span>
            </div>
            <p style="margin: 0; font-size: 0.85rem; color: {COLORS["text_muted"]};">{reason}</p>
        </div>
        """

    return f"""
    <div class="gaps-box">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
            <span class="mdi mdi-file-question" style="color: {COLORS["warning"]}; font-size: 1.25rem;"></span>
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["warning"]};">What We Couldn't Find</h3>
        </div>
        {items}
    </div>
    """


def render_recommendations() -> str:
    """Recommendations."""
    recs = [
        (
            "URGENT",
            "error",
            "mdi-alert-octagon",
            "Monitor Q1 2025 earnings call",
            "April 2025",
        ),
        (
            "STRATEGIC",
            "info",
            "mdi-chess-queen",
            "Evaluate Model 2 timeline",
            "Q2 2025",
        ),
    ]

    items = ""
    for priority, color_key, icon, action, deadline in recs:
        bg = COLORS[f"{color_key}_bg"]
        color = COLORS[color_key]
        items += f"""
        <div class="card" style="margin-bottom: 0.75rem; border-left: 3px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="badge" style="background: {bg}; color: {color};">
                    <span class="mdi {icon}"></span> {priority}
                </span>
                <span style="font-size: 0.75rem; color: {COLORS["text_muted"]};">
                    <span class="mdi mdi-calendar-clock"></span> {deadline}
                </span>
            </div>
            <div style="font-weight: 600; color: {COLORS["text_primary"]};">{action}</div>
        </div>
        """

    return f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
            <span class="mdi mdi-pin" style="color: {COLORS["accent"]}; font-size: 1.25rem;"></span>
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["text_primary"]};">Recommended Actions</h3>
        </div>
        {items}
    </div>
    """


def render_hitl() -> str:
    """HITL checkpoint."""
    return f"""
    <div class="hitl-box">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span class="mdi mdi-account-check" style="color: {COLORS["accent"]}; font-size: 1.25rem;"></span>
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["text_primary"]};">Human Review Checkpoint</h3>
        </div>
        <p style="margin: 0 0 1rem; color: {COLORS["text_secondary"]}; font-size: 0.9rem;">
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
    """Export buttons."""
    return f"""
    <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; padding: 1.5rem 0;">
        <button class="export-btn" style="background: linear-gradient(135deg, #dc2626, #b91c1c); color: white;">
            <span class="mdi mdi-file-pdf-box"></span> Export PDF
        </button>
        <button class="export-btn" style="background: linear-gradient(135deg, #16a34a, #15803d); color: white;">
            <span class="mdi mdi-file-delimited"></span> Export CSV
        </button>
        <button class="export-btn" style="background: {COLORS["bg_elevated"]}; border: 1px solid {COLORS["border"]}; color: {COLORS["text_primary"]};">
            <span class="mdi mdi-content-copy"></span> Copy
        </button>
        <button class="export-btn" style="background: linear-gradient(135deg, {COLORS["info"]}, #2563eb); color: white;">
            <span class="mdi mdi-share-variant"></span> Share
        </button>
    </div>
    """


def render_sources() -> str:
    """Sources tab."""
    cards = ""
    for s in MOCK_SOURCES:
        fresh = '<span class="badge badge-success"><span class="mdi mdi-check-circle"></span> Fresh</span>'
        conf = (
            '<span class="badge badge-success"><span class="mdi mdi-shield-check"></span> High</span>'
            if s["confidence"] == "high"
            else '<span class="badge badge-warning"><span class="mdi mdi-shield-alert"></span> Medium</span>'
        )

        cards += f"""
        <div class="source-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <div>
                    <div style="font-weight: 600; color: {COLORS["text_primary"]};">{s["title"]}</div>
                    <div style="font-size: 0.8rem; color: {COLORS["text_muted"]};">{s["source"]} • {s["date"]}</div>
                </div>
                <div style="display: flex; gap: 0.5rem;">{fresh}{conf}</div>
            </div>
            <div style="background: {COLORS["bg_primary"]}; border-left: 2px solid {COLORS["accent"]}; 
                        padding: 0.5rem 0.75rem; font-size: 0.85rem; color: {COLORS["text_secondary"]}; font-style: italic;">
                "{s["snippet"]}"
            </div>
        </div>
        """

    return f"""
    <div style="{CONTAINER}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["text_primary"]}; display: flex; align-items: center; gap: 0.5rem;">
                <span class="mdi mdi-text-box-multiple" style="color: {COLORS["accent"]};"></span>
                Sources ({len(MOCK_SOURCES)})
            </h3>
            <button class="btn-sm" style="border-style: dashed;">
                <span class="mdi mdi-plus"></span> Add Source
            </button>
        </div>
        {cards}
    </div>
    """


def render_footer() -> str:
    """Footer."""
    return f"""
    <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid {COLORS["border"]}; margin-top: 1rem;">
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
    """Create UI with all fixes."""

    with gr.Blocks() as app:
        # Base
        gr.HTML(render_base())

        # Header with shadow
        gr.HTML(render_header())

        # Research Types (3x2 grid with shadows)
        gr.HTML(render_research_types())

        # Input with Focus Areas and Generate button
        gr.HTML(render_input_section())

        # Progress
        gr.HTML(render_progress())

        # Tabs - wrapped in container for alignment
        gr.HTML(f"<div style='{CONTAINER}'>")
        with gr.Tabs():
            with gr.TabItem("Report"):
                # Report box with header integrated
                gr.HTML(f"""
                    <div class="report-box">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid {COLORS["border"]};">
                            <h3 style="margin: 0; font-size: 1rem; color: {COLORS["text_primary"]}; display: flex; align-items: center; gap: 0.5rem;">
                                <span class="mdi mdi-file-document-outline" style="color: {COLORS["accent"]};"></span>
                                Analysis Report
                            </h3>
                            <span class="badge badge-success"><span class="mdi mdi-check-circle"></span> Complete</span>
                        </div>
                """)
                gr.Markdown(MOCK_REPORT, elem_classes=["report-md"])
                gr.HTML("</div>")

                # Additional sections
                gr.HTML(render_gaps())
                gr.HTML(render_recommendations())
                gr.HTML(render_hitl())

            with gr.TabItem("Sources"):
                gr.HTML(render_sources())
        gr.HTML("</div>")

        # Export
        gr.HTML(render_export())

        # Footer
        gr.HTML(render_footer())

    return app


if __name__ == "__main__":
    app = create_mock_ui()
    print("\n" + "=" * 60)
    print("  MARKET INTELLIGENCE UI v3")
    print("  URL: http://127.0.0.1:7864")
    print("=" * 60 + "\n")
    app.launch(server_name="127.0.0.1", server_port=7864, share=False)
