"""Gradio UI for Market Intelligence System.

F1: Research Type Selection — The gateway feature.
Uses Material Design Icons (MDI) as specified in CLAUDE.md.
"""

import asyncio
import logging
import os
import tempfile
from datetime import datetime

import gradio as gr

from src.utils.logging import setup_logger
from src.workflows.market_analysis import MarketIntelligenceWorkflow
from src.workflows.types import ResearchType

logger = setup_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Material Design Icons (MDI) - CLAUDE.md specification
# ─────────────────────────────────────────────────────────────────────────────

MDI_CDN = (
    "https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css"
)

MDI_ICONS = {
    "domain": "mdi-domain",
    "compare": "mdi-compare",
    "earth": "mdi-earth",
    "sword-cross": "mdi-sword-cross",
    "cash-multiple": "mdi-cash-multiple",
    "help-circle": "mdi-help-circle",
}


# ─────────────────────────────────────────────────────────────────────────────
# Research Type Configuration
# ─────────────────────────────────────────────────────────────────────────────

RESEARCH_TYPE_OPTIONS = {
    "Company Analysis": ResearchType.COMPANY_ANALYSIS,
    "Competitive Comparison": ResearchType.COMPETITIVE_COMPARISON,
    "Market Landscape": ResearchType.MARKET_LANDSCAPE,
    "Battle Card": ResearchType.BATTLE_CARD,
    "Investment Thesis": ResearchType.INVESTMENT_THESIS,
    "Custom Query": ResearchType.CUSTOM_QUERY,
}

RESEARCH_TYPE_META = {
    "Company Analysis": {
        "icon": "domain",
        "desc": "Deep dive on a single company — products, positioning, SWOT",
    },
    "Competitive Comparison": {
        "icon": "compare",
        "desc": "Side-by-side comparison of 2-5 competitors",
    },
    "Market Landscape": {
        "icon": "earth",
        "desc": "Full market overview with players, trends, and entry analysis",
    },
    "Battle Card": {
        "icon": "sword-cross",
        "desc": "1-page sales enablement document",
    },
    "Investment Thesis": {
        "icon": "cash-multiple",
        "desc": "Due diligence report for investors",
    },
    "Custom Query": {
        "icon": "help-circle",
        "desc": "Free-form research question",
    },
}

# Model options for power users who want to test different models
MODEL_OPTIONS = {
    "Grok 3 (Free)": "x-ai/grok-3-fast:free",
    "GPT-4.1 Mini": "openai/gpt-4.1-mini",
    "Claude Sonnet 4": "anthropic/claude-sonnet-4",
    "Gemini 2.5 Flash": "google/gemini-2.5-flash-preview-05-20",
}

# Progress messages - human-readable status updates
PROGRESS_MESSAGES = {
    "starting": "Initializing research agents...",
    "research": "Gathering intelligence from multiple sources...",
    "analysis": "Analyzing competitive landscape and market position...",
    "writing": "Synthesizing insights into actionable report...",
    "complete": "Report ready",
}


# ─────────────────────────────────────────────────────────────────────────────
# Logging Infrastructure (for progress tracking)
# ─────────────────────────────────────────────────────────────────────────────


class ProgressTracker:
    """Tracks workflow progress for user-friendly status updates."""

    def __init__(self) -> None:
        self.current_stage = "starting"
        self.messages: list[str] = []

    def update(self, stage: str) -> None:
        self.current_stage = stage
        if stage in PROGRESS_MESSAGES:
            self.messages.append(PROGRESS_MESSAGES[stage])

    def get_status(self) -> str:
        return PROGRESS_MESSAGES.get(self.current_stage, "Processing...")


class QueueHandler(logging.Handler):
    """Routes logs to progress tracker."""

    def __init__(self, tracker: ProgressTracker) -> None:
        super().__init__()
        self.tracker = tracker

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = record.getMessage().lower()
            if "research" in msg:
                self.tracker.update("research")
            elif "analysis" in msg:
                self.tracker.update("analysis")
            elif "writ" in msg:
                self.tracker.update("writing")
        except Exception:
            pass


def attach_progress_tracker(tracker: ProgressTracker) -> QueueHandler:
    """Attach progress tracker to loggers."""
    handler = QueueHandler(tracker)
    logging.getLogger().addHandler(handler)
    for name, logger_obj in logging.Logger.manager.loggerDict.items():
        if name.startswith("src") and isinstance(logger_obj, logging.Logger):
            logger_obj.addHandler(handler)
    return handler


def detach_progress_tracker(handler: QueueHandler) -> None:
    """Remove progress tracker from loggers."""
    logging.getLogger().removeHandler(handler)
    for name, logger_obj in logging.Logger.manager.loggerDict.items():
        if name.startswith("src") and isinstance(logger_obj, logging.Logger):
            logger_obj.removeHandler(handler)


# ─────────────────────────────────────────────────────────────────────────────
# UI Event Handlers
# ─────────────────────────────────────────────────────────────────────────────


def on_research_type_change(research_type: str) -> tuple[str, dict, dict]:
    """Handle research type selection — show appropriate form with MDI icon."""
    meta = RESEARCH_TYPE_META.get(research_type, {})
    icon = meta.get("icon", "help-circle")
    desc = meta.get("desc", "")

    icon_html = f'<span class="mdi mdi-{icon}" style="font-size:1.2rem;margin-right:0.5rem;"></span>'
    description_html = f"{icon_html} **{research_type}**: {desc}"

    is_company_analysis = research_type == "Company Analysis"

    return (
        description_html,
        gr.update(visible=is_company_analysis),
        gr.update(visible=not is_company_analysis),
    )


async def run_analysis(
    research_type_label: str,
    company_name: str,
    industry: str,
    research_depth: str,
    model_choice: str,
):
    """Execute market intelligence analysis with progress updates."""
    if not company_name:
        yield ("", "Please enter a company name", "⚠️ Missing input")
        return

    research_type = RESEARCH_TYPE_OPTIONS.get(
        research_type_label, ResearchType.COMPANY_ANALYSIS
    )
    model = MODEL_OPTIONS.get(model_choice, "x-ai/grok-3-fast:free")

    # Default budget from env (not user-configurable)
    max_budget = float(os.getenv("MAX_BUDGET", "2.0"))

    tracker = ProgressTracker()
    handler = attach_progress_tracker(tracker)
    tracker.update("starting")

    try:
        workflow = MarketIntelligenceWorkflow(
            max_budget=max_budget,
            model_name=model,
        )

        task = asyncio.create_task(
            workflow.run(
                company_name=company_name,
                industry=industry if industry else None,
                thread_id=f"ui-{datetime.now().timestamp()}",
                research_depth=research_depth.lower(),
                research_type=research_type,
            )
        )

        # Stream progress updates
        while not task.done():
            status = tracker.get_status()
            yield (status, "Generating report...", f"🔄 {status}")
            await asyncio.sleep(0.5)

        result = await task
        tracker.update("complete")

        final_status = (
            "✅ Complete" if not result.get("errors") else "❌ Error occurred"
        )

        yield (
            tracker.get_status(),
            result.get("full_report", "No report generated"),
            final_status,
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        yield ("", f"Error: {e}", "❌ Failed")

    finally:
        detach_progress_tracker(handler)


def download_report(report_content: str) -> str | None:
    """Generate downloadable markdown file."""
    if not report_content:
        return None

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".md", encoding="utf-8"
    ) as f:
        f.write(report_content)
        return f.name


# ─────────────────────────────────────────────────────────────────────────────
# UI Construction
# ─────────────────────────────────────────────────────────────────────────────


def create_ui() -> gr.Blocks:
    """Build the Gradio interface — clean, enterprise-grade."""

    with gr.Blocks() as app:
        # Header
        gr.HTML(f"""
        <link rel="stylesheet" href="{MDI_CDN}">
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid #eee;">
            <h1 style="margin: 0; font-weight: 600;">
                <span class="mdi mdi-chart-timeline-variant"></span>
                Market Intelligence
            </h1>
            <p style="margin: 0.5rem 0 0; color: #666;">
                Enterprise-grade competitive research in minutes
            </p>
        </div>
        """)

        with gr.Row():
            # ─────────────────────────────────────────────────────────────────
            # Left Column: Configuration
            # ─────────────────────────────────────────────────────────────────
            with gr.Column(scale=1):
                # F1: Research Type Selection
                gr.HTML("""
                <h3 style="margin-bottom: 0.5rem;">
                    <span class="mdi mdi-format-list-bulleted-type"></span>
                    What do you need?
                </h3>
                """)
                research_type_selector = gr.Radio(
                    choices=list(RESEARCH_TYPE_OPTIONS.keys()),
                    value="Company Analysis",
                    label="Research Type",
                    show_label=False,
                )
                research_type_description = gr.Markdown(
                    value='<span class="mdi mdi-domain" style="font-size:1.2rem;margin-right:0.5rem;"></span> **Company Analysis**: Deep dive on a single company — products, positioning, SWOT'
                )

                # Dynamic Form: Company Analysis (F2)
                with gr.Group(visible=True) as company_form:
                    company_input = gr.Textbox(
                        label="Company Name",
                        placeholder="e.g., Tesla, Notion, Stripe",
                    )
                    industry_input = gr.Textbox(
                        label="Industry (optional)",
                        placeholder="e.g., Electric Vehicles, SaaS",
                    )
                    research_depth = gr.Radio(
                        choices=["Basic", "Comprehensive"],
                        value="Comprehensive",
                        label="Research Depth",
                        info="Basic: faster, key insights. Comprehensive: deeper analysis.",
                    )

                # Placeholder for F3-F7
                with gr.Group(visible=False) as coming_soon:
                    gr.HTML("""
                    <div style="padding: 2rem; text-align: center; background: #f8f9fa; border-radius: 8px;">
                        <span class="mdi mdi-hammer-wrench" style="font-size: 2rem; color: #666;"></span>
                        <h3>Coming Soon</h3>
                        <p style="color: #666;">This research type is under development.</p>
                    </div>
                    """)

                # Advanced Settings (for power users testing models)
                with gr.Accordion("Advanced Settings", open=False):
                    model_choice = gr.Dropdown(
                        choices=list(MODEL_OPTIONS.keys()),
                        value="Grok 3 (Free)",
                        label="AI Model",
                        info="Test different models for quality comparison",
                    )

                # Run button
                run_btn = gr.Button(
                    "Generate Report",
                    variant="primary",
                    size="lg",
                )

                # Progress indicator
                progress_status = gr.Textbox(
                    label="Status",
                    value="Ready",
                    interactive=False,
                    show_label=False,
                )

            # ─────────────────────────────────────────────────────────────────
            # Right Column: Report Output
            # ─────────────────────────────────────────────────────────────────
            with gr.Column(scale=2):
                gr.HTML("""
                <h3 style="margin-bottom: 1rem;">
                    <span class="mdi mdi-file-document-outline"></span>
                    Report
                </h3>
                """)

                # Single clean output area
                report_display = gr.Markdown(
                    value="Your report will appear here after generation.",
                    elem_id="report-output",
                )

                # Download option
                download_btn = gr.DownloadButton(
                    "Download Report (.md)",
                    visible=True,
                )

        # ─────────────────────────────────────────────────────────────────────
        # Event Wiring
        # ─────────────────────────────────────────────────────────────────────

        research_type_selector.change(
            fn=on_research_type_change,
            inputs=[research_type_selector],
            outputs=[research_type_description, company_form, coming_soon],
        )

        run_btn.click(
            fn=run_analysis,
            inputs=[
                research_type_selector,
                company_input,
                industry_input,
                research_depth,
                model_choice,
            ],
            outputs=[
                progress_status,
                report_display,
                progress_status,
            ],
        )

        download_btn.click(
            fn=download_report,
            inputs=[report_display],
            outputs=[download_btn],
        )

    return app


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    is_deployment = os.getenv("SPACE_ID") or os.getenv("IS_DOCKER")
    server_name = "0.0.0.0" if is_deployment else "127.0.0.1"

    app = create_ui()
    app.launch(server_name=server_name, server_port=7860, share=False, show_error=True)
