"""Market Intelligence UI — Premium Enterprise Design.

F1: Research Type Selection — The gateway feature.
Uses Material Design Icons (MDI) and premium dark theme from app_mock.py.
"""

import os

import gradio as gr

# ─────────────────────────────────────────────────────────────────────────────
# Design System (from app_mock.py — DO NOT MODIFY)
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
# CSS Theme (from app_mock.py — DO NOT MODIFY)
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

/* Primary Button */
button.primary {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, #0d9488 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3) !important;
}}

/* Research Type Cards */
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

/* Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {COLORS["bg_primary"]}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS["border"]}; border-radius: 4px; }}
"""


# ─────────────────────────────────────────────────────────────────────────────
# F1: Research Type Configuration
# ─────────────────────────────────────────────────────────────────────────────

RESEARCH_TYPES = [
    ("Company Analysis", "domain", "Deep dive on a single company"),
    ("Competitive Comparison", "compare", "Compare 2-5 companies"),
    ("Market Landscape", "earth", "Market overview & trends"),
    ("Battle Card", "sword-cross", "Sales enablement"),
    ("Investment Thesis", "cash-multiple", "Due diligence report"),
    ("Custom Query", "help-circle", "Free-form research"),
]


# ─────────────────────────────────────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────────────────────────────────────


def render_base() -> str:
    """Base styles and fonts."""
    return f"""
    <link rel="stylesheet" href="{MDI_CDN}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <style>{THEME_CSS}</style>
    """


def render_header() -> str:
    """Header with logo and title."""
    return f"""
    <div style="background: transparent; padding: 1.25rem 0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
        <div style="{CONTAINER}">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="background: linear-gradient(135deg, {COLORS["accent"]}, #0d9488); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(20, 184, 166, 0.4);">
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
    """F1: Research type cards (3x2 grid)."""
    cards = ""
    for i, (name, icon, desc) in enumerate(RESEARCH_TYPES):
        active = "active" if i == 0 else ""
        cards += f"""
        <div class="research-card {active}" data-index="{i}">
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


def render_coming_soon() -> str:
    """Placeholder for unimplemented features."""
    return f"""
    <div style="{CONTAINER}">
        <div style="padding: 3rem; text-align: center; background: {COLORS["bg_secondary"]}; border: 1px solid {COLORS["border"]}; border-radius: 12px; margin-top: 1rem;">
            <span class="mdi mdi-hammer-wrench" style="font-size: 3rem; color: {COLORS["text_muted"]};"></span>
            <h3 style="margin: 1rem 0 0.5rem; color: {COLORS["text_primary"]};">Coming Soon</h3>
            <p style="margin: 0; color: {COLORS["text_muted"]}; font-size: 0.9rem;">
                Select a research type above. Features are being implemented one at a time.
            </p>
        </div>
    </div>
    """


def render_footer() -> str:
    """Footer with technology credits."""
    return f"""
    <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid {COLORS["border"]}; margin-top: 2rem;">
        <p style="margin: 0; font-size: 0.85rem; color: {COLORS["text_muted"]};">
            <span class="mdi mdi-graph" style="color: {COLORS["accent"]};"></span> LangGraph •
            <span class="mdi mdi-api" style="color: {COLORS["accent"]};"></span> OpenRouter •
            <span class="mdi mdi-magnify" style="color: {COLORS["accent"]};"></span> Tavily
        </p>
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
# Main UI
# ─────────────────────────────────────────────────────────────────────────────


def create_ui() -> gr.Blocks:
    """Build the Gradio interface — F1: Research Type Selection only."""

    with gr.Blocks() as app:
        # Base styles
        gr.HTML(render_base())

        # Header
        gr.HTML(render_header())

        # F1: Research Type Cards
        gr.HTML(render_research_types())

        # Placeholder (F2+ will be added here)
        gr.HTML(render_coming_soon())

        # Footer
        gr.HTML(render_footer())

    return app


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    is_deployment = os.getenv("SPACE_ID") or os.getenv("IS_DOCKER")
    server_name = "0.0.0.0" if is_deployment else "127.0.0.1"

    print("\n" + "=" * 60)
    print("  MARKET INTELLIGENCE")
    print(f"  URL: http://{server_name}:7860")
    print("=" * 60 + "\n")

    app = create_ui()
    app.launch(server_name=server_name, server_port=7860, share=False, show_error=True)
