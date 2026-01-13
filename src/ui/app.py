"""Market Intelligence UI — F2: Company Analysis.

Built with exact design from app_mock.py:
- HTML rendering functions for pixel-perfect visual design
- Hidden Gradio components for workflow wiring
- JavaScript bridge to sync HTML inputs with Gradio state

Run: python -m src.ui.app (or make run)
"""

import asyncio
import os

import gradio as gr

from src.workflows.market_analysis import MarketIntelligenceWorkflow
from src.workflows.types import ResearchType

# ─────────────────────────────────────────────────────────────────────────────
# Design System (exact copy from app_mock.py)
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
CONTAINER = "max-width: 900px; margin: 0 auto; padding: 0 1.5rem;"

# ─────────────────────────────────────────────────────────────────────────────
# CSS (exact copy from app_mock.py)
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

/* Research Type Cards */
.research-type-container {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
}}

.research-type-card {{
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

.research-type-card:hover {{
    border-color: {COLORS["accent"]};
    background: {COLORS["bg_elevated"]};
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}}

.research-type-card.selected {{
    border-color: {COLORS["accent"]};
    background: {COLORS["accent_muted"]};
    box-shadow: 0 0 0 3px {COLORS["accent_muted"]}, 0 8px 24px rgba(20, 184, 166, 0.2);
}}

.research-type-icon {{
    width: 36px;
    height: 36px;
    min-width: 36px;
    background: {COLORS["accent_muted"]};
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.research-type-icon .mdi {{
    font-size: 1.25rem;
    color: {COLORS["accent"]};
}}

.research-type-title {{
    font-weight: 600;
    font-size: 0.9rem;
    color: {COLORS["text_primary"]};
    margin-bottom: 0.125rem;
}}

.research-type-desc {{
    font-size: 0.75rem;
    color: {COLORS["text_muted"]};
    line-height: 1.3;
}}

/* Focus Areas Accordion */
.focus-areas {{
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
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

/* Report content */
.report-box {{
    background: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 1.5rem;
}}

.report-md h2 {{
    color: {COLORS["text_primary"]};
    font-size: 1.25rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {COLORS["border"]};
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
}}

/* Tabs */
.tabs {{
    {CONTAINER}
}}

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

/* Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {COLORS["bg_primary"]}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS["border"]}; border-radius: 4px; }}

/* Animations */
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}

/* Gradio overrides */
input[type="text"], textarea {{
    background: {COLORS["bg_secondary"]} !important;
    border: 1px solid {COLORS["border"]} !important;
    border-radius: 10px !important;
    color: {COLORS["text_primary"]} !important;
}}

button.primary, button.lg {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, #0d9488 100%) !important;
    border: none !important;
    height: 48px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3) !important;
}}

.btn-sm {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    height: 36px;
    padding: 0 0.875rem;
    background: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    color: {COLORS["text_muted"]};
    font-size: 0.85rem;
    cursor: pointer;
}}

.export-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    height: 40px;
    padding: 0 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
}}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────────────────────────────────────

RESEARCH_TYPES = [
    ("Company Analysis", "domain", "Deep dive on a single company"),
    ("Competitive Comparison", "compare", "Compare 2-5 companies"),
    ("Market Landscape", "earth", "Market overview & trends"),
    ("Battle Card", "sword-cross", "Sales enablement"),
    ("Investment Thesis", "cash-multiple", "Due diligence report"),
    ("Custom Query", "help-circle", "Free-form research"),
]

FOCUS_AREAS = [
    ("Products & Services", "Product offerings, features, portfolio", True),
    ("Pricing", "Pricing models, tiers, positioning", False),
    ("Leadership", "Executive team, board, org structure", False),
    ("Financials", "Revenue, margins, funding, health", True),
    ("Market Position", "Market share, competitive landscape", True),
]


# ─────────────────────────────────────────────────────────────────────────────
# HTML Rendering Functions (from app_mock.py)
# ─────────────────────────────────────────────────────────────────────────────


def render_base() -> str:
    """Base styles and fonts."""
    return f"""
    <link rel="stylesheet" href="{MDI_CDN}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <style>{THEME_CSS}</style>
    """


def render_header() -> str:
    """Header with logo."""
    return f"""
    <div style="background: transparent; padding: 1.25rem 0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
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
    """Research type selection cards."""
    cards = ""
    for i, (name, icon, desc) in enumerate(RESEARCH_TYPES):
        selected = "selected" if i == 0 else ""
        cards += f"""
        <div class="research-type-card {selected}" data-index="{i}">
            <div class="research-type-icon">
                <span class="mdi mdi-{icon}"></span>
            </div>
            <div>
                <div class="research-type-title">{name}</div>
                <div class="research-type-desc">{desc}</div>
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
            <div class="research-type-container">
                {cards}
            </div>
        </div>
    </div>
    """


def create_focus_areas_html() -> str:
    """Focus area checkboxes content."""
    items = ""
    for name, desc, checked in FOCUS_AREAS:
        checked_attr = "checked" if checked else ""
        items += f"""
        <label class="focus-checkbox">
            <input type="checkbox" {checked_attr}>
            <div>
                <div style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.9rem;">{name}</div>
                <div style="font-size: 0.75rem; color: {COLORS["text_muted"]};">{desc}</div>
            </div>
        </label>
        """
    return items


def render_input_section() -> str:
    """Company input with focus areas accordion."""
    return f"""
    <div style="padding: 0 0 1.5rem;">
        <div style="{CONTAINER}">
            <!-- Company Input -->
            <div style="margin-bottom: 1rem;">
                <label style="display: block; margin-bottom: 0.5rem; font-size: 0.85rem; color: {COLORS["text_secondary"]}; font-weight: 500;">
                    Company Name
                </label>
                <div style="position: relative;">
                    <input type="text" id="company-input" placeholder="Enter company name..."
                           style="width: 100%; height: 48px; padding: 0 1rem 0 3rem; font-size: 1rem;
                                  background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]};
                                  border-radius: 10px; color: {COLORS["text_primary"]};">
                    <span class="mdi mdi-magnify" style="position: absolute; right: 1rem; top: 50%;
                          transform: translateY(-50%); color: {COLORS["text_muted"]}; font-size: 1.25rem;"></span>
                </div>
            </div>

            <!-- Focus Areas Accordion -->
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
                    {create_focus_areas_html()}
                </div>
            </details>

            <!-- Advanced Settings -->
            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                <button class="btn-sm"><span class="mdi mdi-cog"></span> Advanced Settings</button>
            </div>

            <!-- Generate Button -->
            <button id="generate-btn" style="width: 100%; height: 48px; margin-top: 1rem;
                           background: linear-gradient(135deg, {COLORS["accent"]}, #0d9488);
                           border: none; border-radius: 10px; color: white; font-weight: 600; font-size: 1rem;
                           cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem;
                           box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);">
                <span class="mdi mdi-play"></span> Generate Report
            </button>
        </div>
    </div>
    """


def render_progress(visible: bool = False, progress: int = 0, status: str = "") -> str:
    """Progress indicator (hidden by default)."""
    display = "block" if visible else "none"
    return f"""
    <div id="progress-section" style="display: {display}; padding: 0 0 0.8rem;">
        <div style="{CONTAINER}">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span class="mdi mdi-loading" style="color: {COLORS["accent"]}; font-size: 1rem; animation: spin 1s linear infinite;"></span>
                <span style="color: {COLORS["text_secondary"]}; font-size: 0.9rem;">{status}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%;"></div>
            </div>
        </div>
    </div>
    """


def render_report(report_html: str) -> str:
    """Report display inside card container."""
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


def render_sources(sources: list) -> str:
    """Sources list."""
    if not sources:
        return f"""
        <div style="text-align: center; padding: 2rem; color: {COLORS["text_muted"]};">
            <span class="mdi mdi-file-search" style="font-size: 2rem;"></span>
            <p>No sources yet. Generate a report to see sources.</p>
        </div>
        """

    cards = ""
    for s in sources:
        title = s.get("title", "Source")
        content = s.get("content", "")[:150] + "..." if s.get("content") else ""

        cards += f"""
        <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem;
                    border-bottom: 1px solid {COLORS["border"]};">
            <span class="mdi mdi-file-document-outline" style="color: {COLORS["accent"]}; font-size: 0.9rem;"></span>
            <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 500; color: {COLORS["text_primary"]}; font-size: 0.85rem;">{title}</div>
                <div style="font-size: 0.75rem; color: {COLORS["text_muted"]}; margin-top: 0.25rem;">{content}</div>
            </div>
        </div>
        """

    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <h3 style="margin: 0; font-size: 0.95rem; color: {COLORS["text_primary"]}; display: flex; align-items: center; gap: 0.5rem;">
            <span class="mdi mdi-text-box-multiple" style="color: {COLORS["accent"]};"></span>
            Sources ({len(sources)})
        </h3>
    </div>
    <div style="background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]}; border-radius: 10px; max-height: 500px; overflow-y: auto;">
        {cards}
    </div>
    """


def render_footer() -> str:
    """Footer with technology credits."""
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


async def run_workflow(company_name: str, industry: str | None = None) -> dict:
    """Execute the market intelligence workflow."""
    workflow = MarketIntelligenceWorkflow(checkpoint_path=":memory:")
    result = await workflow.run(
        company_name=company_name,
        industry=industry,
        research_type=ResearchType.COMPANY_ANALYSIS,
    )
    return result


def generate_report(company_name: str) -> tuple[str, str]:
    """
    Handler for Generate Report button.

    Returns:
        Tuple of (report_html, sources_html)
    """
    if not company_name or not company_name.strip():
        return (
            f"<div style='color: {COLORS['warning']}; padding: 1rem;'>"
            "<span class='mdi mdi-alert'></span> Please enter a company name.</div>",
            "",
        )

    try:
        # Run the async workflow
        result = asyncio.run(run_workflow(company_name.strip()))

        # Convert markdown to HTML
        import markdown  # type: ignore[import-untyped]

        md = markdown.Markdown(extensions=["tables", "fenced_code"])
        report_md = result.get("full_report", "No report generated.")
        report_html = md.convert(report_md)

        # Get sources
        sources = result.get("raw_sources", [])

        return render_report(report_html), render_sources(sources)

    except Exception as e:
        error_html = f"""
        <div style="color: {COLORS["error"]}; padding: 1rem; background: {COLORS["error_bg"]}; border-radius: 10px;">
            <span class="mdi mdi-alert-circle"></span> Error: {str(e)}
        </div>
        """
        return error_html, ""


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────


def create_ui() -> gr.Blocks:
    """Build the Gradio interface."""

    with gr.Blocks() as app:
        # Base styles
        gr.HTML(render_base())

        # Header
        gr.HTML(render_header())

        # Research Types (HTML cards)
        gr.HTML(render_research_types())

        # Input Section (HTML with JavaScript bridge)
        gr.HTML(render_input_section())

        # Report/Sources Tabs
        gr.HTML(f"<div style='{CONTAINER}'>")
        with gr.Tabs():
            with gr.TabItem("Report"):
                report_output = gr.HTML(
                    value=f"<div style='text-align: center; padding: 2rem; color: {COLORS['text_muted']};'>"
                    "<span class='mdi mdi-file-document-outline' style='font-size: 2rem;'></span>"
                    "<p>Enter a company name and click Generate Report.</p></div>"
                )

            with gr.TabItem("Sources"):
                sources_output = gr.HTML(value=render_sources([]))
        gr.HTML("</div>")

        # Hidden Gradio components for workflow wiring
        company_hidden = gr.Textbox(value="", visible=False, elem_id="company-hidden")
        generate_hidden = gr.Button("Generate", visible=False, elem_id="generate-hidden")

        # Wire the hidden button to the workflow
        generate_hidden.click(
            fn=generate_report,
            inputs=[company_hidden],
            outputs=[report_output, sources_output],
        )

        # JavaScript bridge - wait for Gradio to render, then connect
        gr.HTML("""
        <script>
        // Wait for Gradio to fully render, then setup the bridge
        function setupBridge() {
            const companyInput = document.getElementById('company-input');
            const generateBtn = document.getElementById('generate-btn');

            // Find hidden Gradio components (Gradio 6.x structure)
            const hiddenTextarea = document.querySelector('#company-hidden input, #company-hidden textarea');
            const hiddenButton = document.querySelector('#generate-hidden button');

            if (!companyInput || !generateBtn) {
                console.log('Waiting for HTML elements...');
                setTimeout(setupBridge, 100);
                return;
            }

            if (!hiddenTextarea || !hiddenButton) {
                console.log('Waiting for Gradio hidden components...');
                setTimeout(setupBridge, 100);
                return;
            }

            console.log('Bridge connected!');

            // Sync input value on every keystroke
            companyInput.addEventListener('input', (e) => {
                hiddenTextarea.value = e.target.value;
                hiddenTextarea.dispatchEvent(new Event('input', { bubbles: true }));
            });

            // Sync on blur for safety
            companyInput.addEventListener('blur', (e) => {
                hiddenTextarea.value = e.target.value;
                hiddenTextarea.dispatchEvent(new Event('input', { bubbles: true }));
            });

            // Click hidden button when HTML button is clicked
            generateBtn.addEventListener('click', (e) => {
                e.preventDefault();
                // Final sync before click
                hiddenTextarea.value = companyInput.value;
                hiddenTextarea.dispatchEvent(new Event('input', { bubbles: true }));
                // Small delay to ensure value is set
                setTimeout(() => hiddenButton.click(), 50);
            });
        }

        // Start setup when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => setTimeout(setupBridge, 500));
        } else {
            setTimeout(setupBridge, 500);
        }
        </script>
        """)

        # Footer
        gr.HTML(render_footer())

    return app


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    is_deploy = os.getenv("SPACE_ID") or os.getenv("IS_DOCKER")
    server = "0.0.0.0" if is_deploy else "127.0.0.1"

    print("\n" + "=" * 60)
    print("  MARKET INTELLIGENCE — F2: Company Analysis")
    print(f"  URL: http://{server}:7860")
    print("=" * 60 + "\n")

    ui = create_ui()
    ui.launch(server_name=server, server_port=7860, share=False, show_error=True)
