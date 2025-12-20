"""Analysis Agent for competitive intelligence and SWOT analysis."""

from typing import Optional

from src.agents.base import BaseAgent
from src.utils.cost_tracker import CostTracker
from src.utils.logging import setup_logger
from src.utils.prompts import (
    ANALYST_COMPETITIVE_MATRIX,
    ANALYST_POSITIONING,
    ANALYST_RECOMMENDATIONS,
    ANALYST_SWOT,
    ANALYST_SYSTEM,
)
from src.workflows.types import AnalysisOutput, ResearchOutput

logger = setup_logger(__name__)


class AnalysisAgent(BaseAgent):
    """
    Analysis Agent responsible for strategic business analysis.

    Takes research data and produces:
    - SWOT analysis
    - Competitive matrix
    - Market positioning analysis
    - Strategic recommendations
    """

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.4,  # Balanced for analytical reasoning
        cost_tracker: Optional[CostTracker] = None,
    ):
        """
        Initialize Analysis Agent.

        Args:
            model: LLM model to use
            temperature: Sampling temperature
            cost_tracker: Cost tracker instance
        """
        super().__init__(
            name="AnalysisAgent",
            model=model,
            temperature=temperature,
            cost_tracker=cost_tracker,
        )

    def get_system_prompt(self) -> str:
        """Get system prompt for analysis agent."""
        return ANALYST_SYSTEM

    async def run(  # type: ignore[override]
        self,
        research_data: ResearchOutput,
    ) -> AnalysisOutput:
        """
        Perform comprehensive analysis on research data.

        Args:
            research_data: Output from ResearchAgent containing:
                - company_overview
                - competitors
                - market_trends

        Returns:
            Dictionary with analysis results:
                - swot: SWOT analysis
                - competitive_matrix: Competitor comparison
                - positioning: Market positioning analysis
                - strategic_recommendations: Action items
        """
        company_name = research_data["company_name"]
        logger.info(f"Starting analysis for: {company_name}")

        results: AnalysisOutput = {
            "company_name": company_name,
            "swot": "",
            "competitive_matrix": "",
            "positioning": "",
            "strategic_recommendations": "",
        }

        try:
            # 1. SWOT Analysis
            swot = await self._perform_swot_analysis(research_data)
            results["swot"] = swot

            # 2. Competitive Matrix
            matrix = await self._create_competitive_matrix(research_data)
            results["competitive_matrix"] = matrix

            # 3. Market Positioning
            positioning = await self._analyze_market_positioning(research_data)
            results["positioning"] = positioning

            # 4. Strategic Recommendations
            recommendations = await self._generate_recommendations(research_data, swot)
            results["strategic_recommendations"] = recommendations

            logger.info(f"Analysis complete for {company_name}")

            return results

        except Exception as e:
            logger.error(f"Analysis failed for {company_name}: {e}")
            raise

    async def _perform_swot_analysis(
        self,
        research_data: ResearchOutput,
    ) -> str:
        """Generate SWOT analysis from research data."""
        user_message = ANALYST_SWOT.format(
            company_name=research_data.get("company_name"),
            company_overview=research_data.get("company_overview", ""),
            competitors=research_data.get("competitors", ""),
            market_trends=research_data.get("market_trends", ""),
        )
        return await self._invoke_llm(self._create_messages(user_message))

    async def _create_competitive_matrix(
        self,
        research_data: ResearchOutput,
    ) -> str:
        """Create competitive comparison matrix."""
        user_message = ANALYST_COMPETITIVE_MATRIX.format(
            company_name=research_data.get("company_name"),
            competitors_info=research_data.get("competitors", ""),
        )
        return await self._invoke_llm(self._create_messages(user_message))

    async def _analyze_market_positioning(
        self,
        research_data: ResearchOutput,
    ) -> str:
        """Analyze market positioning strategy."""
        user_message = ANALYST_POSITIONING.format(
            company_name=research_data.get("company_name"),
            company_overview=research_data.get("company_overview", ""),
            competitors=research_data.get("competitors", ""),
        )
        return await self._invoke_llm(self._create_messages(user_message))

    async def _generate_recommendations(
        self,
        research_data: ResearchOutput,
        swot: str,
    ) -> str:
        """Generate strategic recommendations."""
        user_message = ANALYST_RECOMMENDATIONS.format(
            company_name=research_data.get("company_name"),
            swot=swot,
            market_trends=research_data.get("market_trends", ""),
        )
        return await self._invoke_llm(self._create_messages(user_message))
