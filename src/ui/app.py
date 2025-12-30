"""Gradio UI for Market Intelligence System.

F1: Research Type Selection — The gateway feature.
Uses Material Design Icons (MDI) as specified in CLAUDE.md.
"""

import asyncio
import logging
import os
import queue
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

# Icon mapping per CLAUDE.md Icon Reference
MDI_ICONS = {
    "domain": "mdi-domain",  # Company
    "compare": "mdi-compare",  # Competitive Comparison
    "earth": "mdi-earth",  # Market Landscape
    "sword-cross": "mdi-sword-cross",  # Battle Card
    "cash-multiple": "mdi-cash-multiple",  # Investment
    "help-circle": "mdi-help-circle",  # Custom Query
}


def mdi(icon: str, label: str) -> str:
    """Create MDI icon + label for Gradio radio buttons."""
    icon_class = MDI_ICONS.get(icon, f"mdi-{icon}")
    return f'<span class="mdi {icon_class}"></span> {label}'


# ─────────────────────────────────────────────────────────────────────────────
# Research Type Configuration
# ─────────────────────────────────────────────────────────────────────────────

# Using text labels with icon indicators - Gradio Radio doesn't render HTML in choices
# We'll add visual icons via custom CSS and the description area
RESEARCH_TYPE_OPTIONS = {
    "Company Analysis": ResearchType.COMPANY_ANALYSIS,
    "Competitive Comparison": ResearchType.COMPETITIVE_COMPARISON,
    "Market Landscape": ResearchType.MARKET_LANDSCAPE,
    "Battle Card": ResearchType.BATTLE_CARD,
    "Investment Thesis": ResearchType.INVESTMENT_THESIS,
    "Custom Query": ResearchType.CUSTOM_QUERY,
}

# Icons and descriptions per research type
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

MODEL_OPTIONS = {
    "Grok 4.1 Fast (Free)": "x-ai/grok-4.1-fast:free",
    "GPT-5 Mini (Cheap)": "openai/gpt-5-mini",
    "Claude Sonnet 4.5 (Best) - Temporarily Unavailable": "anthropic/claude-sonnet-4.5",
    "Gemini 2.5 Flash Lite (Fast)": "google/gemini-2.5-flash-lite",
}


# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS with MDI Integration
# ─────────────────────────────────────────────────────────────────────────────

CUSTOM_CSS = """
/* Import Material Design Icons */
@import url('https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css');

/* Research type icon display */
.research-icon {
    font-size: 1.5rem;
    margin-right: 0.5rem;
    vertical-align: middle;
}

/* Description styling */
.research-description {
    padding: 0.75rem 1rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 8px;
    border-left: 4px solid #667eea;
    margin-top: 0.5rem;
}

/* Coming soon banner */
.coming-soon {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Logging Infrastructure
# ─────────────────────────────────────────────────────────────────────────────


class QueueHandler(logging.Handler):
    """Routes logs to a queue for real-time streaming."""

    def __init__(self, log_queue: queue.Queue[str]) -> None:
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if record.name.startswith("src."):
                record.name = record.name[4:]
            self.log_queue.put(self.format(record))
        except Exception:
            self.handleError(record)


def setup_log_streaming() -> tuple[queue.Queue[str], QueueHandler]:
    """Configure log streaming to a queue."""
    log_queue: queue.Queue[str] = queue.Queue()
    handler = QueueHandler(log_queue)
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    return log_queue, handler


def attach_log_handler(handler: QueueHandler) -> None:
    """Attach handler to root and all src.* loggers."""
    logging.getLogger().addHandler(handler)
    for name, logger_obj in logging.Logger.manager.loggerDict.items():
        if name.startswith("src") and isinstance(logger_obj, logging.Logger):
            logger_obj.addHandler(handler)


def detach_log_handler(handler: QueueHandler) -> None:
    """Remove handler from all loggers."""
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

    # Build description with MDI icon
    icon_html = f'<span class="mdi mdi-{icon} research-icon"></span>'
    description_html = f"{icon_html} **{research_type}**: {desc}"

    # Only Company Analysis is fully implemented (F2-F7 coming later)
    is_company_analysis = research_type == "Company Analysis"

    return (
        description_html,
        gr.update(visible=is_company_analysis),
        gr.update(visible=not is_company_analysis),
    )


def validate_model_selection(model_name: str) -> str:
    """Validate model availability."""
    if "Temporarily Unavailable" in model_name:
        gr.Warning("This model is temporarily unavailable. Please select another.")
        return "Grok 4.1 Fast (Free)"
    return model_name


def clear_inputs() -> tuple[str, str, str, str, str, float]:
    """Reset all inputs to defaults."""
    return (
        "Company Analysis",
        "",
        "",
        "Comprehensive",
        "Grok 4.1 Fast (Free)",
        0.5,
    )


async def run_analysis(
    research_type_label: str,
    company_name: str,
    industry: str,
    model_choice: str,
    max_budget: float,
    research_depth: str,
):
    """Execute market intelligence analysis with live logging."""
    if not company_name:
        yield ("Please enter a company name", "", 0.0, "⚠️ Missing input", "")
        return

    research_type = RESEARCH_TYPE_OPTIONS.get(
        research_type_label, ResearchType.COMPANY_ANALYSIS
    )
    model = MODEL_OPTIONS.get(model_choice, "x-ai/grok-4.1-fast:free")

    log_queue, handler = setup_log_streaming()
    attach_log_handler(handler)

    logs: list[str] = []

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

        while not task.done():
            while not log_queue.empty():
                try:
                    logs.append(log_queue.get_nowait())
                except queue.Empty:
                    break

            yield (
                "\n".join(logs),
                "Analysis in progress...",
                0.0,
                "🔄 Running...",
                "Generating summary...",
            )
            await asyncio.sleep(0.1)

        result = await task
        while not log_queue.empty():
            try:
                logs.append(log_queue.get_nowait())
            except queue.Empty:
                break

        status = (
            f"✅ Complete - ${result['total_cost']:.4f}"
            if not result.get("errors")
            else "❌ Failed"
        )

        yield (
            "\n".join(logs),
            result.get("full_report", "No report generated"),
            result.get("total_cost", 0.0),
            status,
            result.get("executive_summary", ""),
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        yield (f"Error: {e}", "", 0.0, f"❌ Failed: {e}", "")

    finally:
        detach_log_handler(handler)


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
    """Build the Gradio interface with MDI icons."""

    with gr.Blocks() as app:
        # Header with MDI
        gr.HTML(f"""
        <link rel="stylesheet" href="{MDI_CDN}">
        <div style="text-align: center; padding: 1rem 0;">
            <h1><span class="mdi mdi-rocket-launch"></span> Agentic Market Research</h1>
            <p style="font-size: 1.1rem; color: #666;">
                80x faster, 2000x cheaper market intelligence — powered by LangGraph
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
                <h3><span class="mdi mdi-format-list-bulleted-type"></span> What do you need?</h3>
                """)
                research_type_selector = gr.Radio(
                    choices=list(RESEARCH_TYPE_OPTIONS.keys()),
                    value="Company Analysis",
                    label="Research Type",
                    info="Select the type of research to perform",
                )
                research_type_description = gr.Markdown(
                    value='<span class="mdi mdi-domain research-icon"></span> **Company Analysis**: Deep dive on a single company — products, positioning, SWOT',
                    elem_classes=["research-description"],
                )

                gr.HTML("<hr style='margin: 1rem 0;'>")

                # Dynamic Form: Company Analysis (F2)
                with gr.Group(visible=True) as company_form:
                    gr.HTML("""
                    <h3><span class="mdi mdi-pencil"></span> Analysis Target</h3>
                    """)
                    company_input = gr.Textbox(
                        label="Company/Product Name",
                        placeholder="e.g., Tesla, Notion, Stripe",
                        info="The company or product to analyze",
                    )
                    industry_input = gr.Textbox(
                        label="Industry (optional)",
                        placeholder="e.g., Electric Vehicles, SaaS",
                        info="Helps contextualize the analysis",
                    )
                    research_depth = gr.Radio(
                        choices=["Basic", "Comprehensive"],
                        value="Comprehensive",
                        label="Research Depth",
                        info="Basic: faster. Comprehensive: deeper.",
                    )

                # Placeholder for F3-F7 (Coming Soon)
                with gr.Group(visible=False) as coming_soon:
                    gr.HTML("""
                    <div class="coming-soon">
                        <h3><span class="mdi mdi-hammer-wrench"></span> Coming Soon</h3>
                        <p>This research type is coming in a future update.</p>
                        <p>For now, try <strong>Company Analysis</strong> to see the full workflow.</p>
                    </div>
                    """)

                # Advanced Settings
                with gr.Accordion("⚙️ Advanced Settings", open=False):
                    model_choice = gr.Dropdown(
                        choices=list(MODEL_OPTIONS.keys()),
                        value="Grok 4.1 Fast (Free)",
                        label="AI Model",
                        info="Free models for testing, paid for production",
                    )
                    budget_slider = gr.Slider(
                        minimum=0.1,
                        maximum=2.0,
                        value=0.5,
                        step=0.1,
                        label="Max Budget (USD)",
                        info="Strict limit: $2.00 max",
                    )

                # Action Buttons
                run_btn = gr.Button("🚀 Run Analysis", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary")

                # Cost Display
                gr.HTML("""
                <h3><span class="mdi mdi-currency-usd"></span> Cost</h3>
                """)
                cost_display = gr.Number(label="Run Cost ($)", value=0, precision=4)
                budget_status = gr.Textbox(
                    label="Status", value="Ready", interactive=False
                )

            # ─────────────────────────────────────────────────────────────────
            # Right Column: Results
            # ─────────────────────────────────────────────────────────────────
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.TabItem("🤖 Activity Log"):
                        activity_log = gr.Textbox(
                            label="Live Activity",
                            lines=20,
                            max_lines=30,
                            interactive=False,
                            show_label=False,
                            autoscroll=True,
                        )

                    with gr.TabItem("📋 Executive Summary"):
                        exec_summary = gr.Textbox(
                            label="Summary",
                            lines=30,
                            max_lines=50,
                            interactive=False,
                            show_label=False,
                        )

                    with gr.TabItem("📊 Full Report"):
                        report_display = gr.Markdown()

                    with gr.TabItem("📥 Download"):
                        gr.Markdown("### Download Report")
                        download_btn = gr.DownloadButton("Download Report (Markdown)")

        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; 
                    border-top: 1px solid #eee; color: #666;">
            <p><strong>Agentic Market Research</strong></p>
            <p><span class="mdi mdi-graph"></span> LangGraph 
               <span class="mdi mdi-api"></span> OpenRouter 
               <span class="mdi mdi-magnify"></span> Tavily</p>
        </div>
        """)

        # ─────────────────────────────────────────────────────────────────────
        # Event Wiring
        # ─────────────────────────────────────────────────────────────────────

        research_type_selector.change(
            fn=on_research_type_change,
            inputs=[research_type_selector],
            outputs=[research_type_description, company_form, coming_soon],
        )

        model_choice.change(
            fn=validate_model_selection,
            inputs=[model_choice],
            outputs=[model_choice],
        )

        clear_btn.click(
            fn=clear_inputs,
            outputs=[
                research_type_selector,
                company_input,
                industry_input,
                research_depth,
                model_choice,
                budget_slider,
            ],
        )

        run_btn.click(
            fn=run_analysis,
            inputs=[
                research_type_selector,
                company_input,
                industry_input,
                model_choice,
                budget_slider,
                research_depth,
            ],
            outputs=[
                activity_log,
                report_display,
                cost_display,
                budget_status,
                exec_summary,
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
