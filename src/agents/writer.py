"""Writer Agent for generating professional market intelligence reports."""

from datetime import datetime
from typing import Optional

from src.agents.base import BaseAgent
from src.utils.cost_tracker import CostTracker
from src.utils.logging import setup_logger
from src.utils.prompts import (
    WRITER_EXECUTIVE_SUMMARY,
    WRITER_FULL_REPORT,
    WRITER_SYSTEM,
)
from src.workflows.types import AnalysisOutput, ReportOutput, ResearchOutput

logger = setup_logger(__name__)


class WriterAgent(BaseAgent):
    """
    Writer Agent responsible for generating final reports.

    Takes research and analysis data and creates:
    - Executive summary
    - Comprehensive market intelligence report
    - Properly formatted markdown with citations
    """

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.6,  # Higher for better writing quality
        cost_tracker: Optional[CostTracker] = None,
    ):
        """
        Initialize Writer Agent.

        Args:
            model: LLM model to use
            temperature: Sampling temperature
            cost_tracker: Cost tracker instance
        """
        super().__init__(
            name="WriterAgent",
            model=model,
            temperature=temperature,
            cost_tracker=cost_tracker,
        )

    def get_system_prompt(self) -> str:
        """Get system prompt for writer agent."""
        return WRITER_SYSTEM

    async def run(  # type: ignore[override]
        self,
        research_data: ResearchOutput,
        analysis_data: AnalysisOutput,
    ) -> ReportOutput:
        """
        Generate comprehensive market intelligence report.

        Args:
            research_data: Output from ResearchAgent
            analysis_data: Output from AnalysisAgent

        Returns:
            Dictionary with report components:
                - executive_summary: Brief overview
                - full_report: Complete markdown report
                - metadata: Report metadata (date, sources count, etc.)
        """
        company_name = research_data.get("company_name")
        logger.info(f"Starting report generation for: {company_name}")

        try:
            # Generate report sections
            exec_summary = await self._write_executive_summary(
                research_data, analysis_data
            )

            full_report = await self._write_full_report(
                research_data, analysis_data, exec_summary
            )

            # Gather metadata
            metadata = {
                "company_name": company_name,
                "industry": research_data.get("industry"),
                "generated_date": datetime.now().isoformat(),
                "sources_count": len(research_data.get("raw_sources", [])),
                "model_used": self.model_name,
            }

            logger.info(f"Report generation complete for {company_name}")

            return {
                "executive_summary": exec_summary,
                "full_report": full_report,
                "metadata": metadata,
            }

        except Exception as e:
            logger.error(f"Report generation failed for {company_name}: {e}")
            raise

    async def _write_executive_summary(
        self,
        research_data: ResearchOutput,
        analysis_data: AnalysisOutput,
    ) -> str:
        """Write executive summary (200-300 words)."""
        user_message = WRITER_EXECUTIVE_SUMMARY.format(
            company_name=research_data.get("company_name"),
            company_overview=research_data.get("company_overview", ""),
            swot=analysis_data.get("swot", ""),
            strategic_recommendations=analysis_data.get(
                "strategic_recommendations", ""
            ),
        )
        return await self._invoke_llm(self._create_messages(user_message))

    async def _write_full_report(
        self,
        research_data: ResearchOutput,
        analysis_data: AnalysisOutput,
        exec_summary: str,
    ) -> str:
        """Write complete markdown report."""
        company_name = research_data.get("company_name")

        user_message = WRITER_FULL_REPORT.format(
            company_name=company_name,
            exec_summary=exec_summary,
            company_overview=research_data.get("company_overview", ""),
            competitors=research_data.get("competitors", ""),
            competitive_matrix=analysis_data.get("competitive_matrix", ""),
            swot=analysis_data.get("swot", ""),
            positioning=analysis_data.get("positioning", ""),
            market_trends=research_data.get("market_trends", ""),
            strategic_recommendations=analysis_data.get(
                "strategic_recommendations", ""
            ),
            date=datetime.now().strftime("%B %d, %Y"),
        )
        return await self._invoke_llm(self._create_messages(user_message))
