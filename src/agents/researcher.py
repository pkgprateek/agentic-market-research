"""Research Agent for gathering market intelligence data."""

from typing import Optional

from src.agents.base import BaseAgent
from src.tools.search import TavilySearchTool
from src.utils.cost_tracker import CostTracker
from src.utils.logging import setup_logger
from src.utils.prompts import (
    RESEARCHER_ANALYZE_COMPANY,
    RESEARCHER_ANALYZE_COMPETITORS,
    RESEARCHER_ANALYZE_TRENDS,
    RESEARCHER_SYSTEM,
)
from src.workflows.types import ResearchOutput

logger = setup_logger(__name__)


class ResearchAgent(BaseAgent):
    """
    Research Agent responsible for gathering data from web sources.

    Uses Tavily API for web search and can gather:
    - Company information
    - Competitor analysis data
    - Market trends and insights
    - Industry news
    """

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.3,  # Lower for more factual responses
        cost_tracker: Optional[CostTracker] = None,
    ):
        """
        Initialize Research Agent.

        Args:
            model: LLM model to use
            temperature: Sampling temperature (lower for research)
            cost_tracker: Cost tracker instance
        """
        super().__init__(
            name="ResearchAgent",
            model=model,
            temperature=temperature,
            cost_tracker=cost_tracker,
        )

        self.search_tool = TavilySearchTool()

    def get_system_prompt(self) -> str:
        """Get system prompt for research agent."""
        return RESEARCHER_SYSTEM

    async def run(  # type: ignore[override]
        self,
        company_name: str,
        industry: Optional[str] = None,
        research_depth: str = "comprehensive",
    ) -> ResearchOutput:
        """
        Gather research data about a company.

        Args:
            company_name: Target company name
            industry: Optional industry context
            research_depth: "basic" or "comprehensive"

        Returns:
            Dictionary with research results:
                - company_overview: Company information
                - competitors: Competitor analysis
                - market_trends: Industry trends
                - raw_sources: List of sources used
        """
        logger.info(f"Starting research for: {company_name}")

        results: ResearchOutput = {
            "company_name": company_name,
            "industry": industry,
            "company_overview": "",
            "competitors": "",
            "market_trends": "",
            "raw_sources": [],
        }

        try:
            # 1. Company Overview
            company_data = await self.search_tool.get_company_info(
                company_name=company_name,
                max_results=10 if research_depth == "comprehensive" else 5,
            )

            results["raw_sources"].extend(company_data.get("results", []))

            # Analyze company data with LLM
            company_context = self.search_tool.format_results_for_llm(company_data)
            company_analysis = await self._analyze_company(
                company_name, company_context
            )
            results["company_overview"] = company_analysis

            # 2. Competitor Analysis
            competitor_data = await self.search_tool.get_competitor_info(
                company_name=company_name,
                industry=industry,
                max_results=10 if research_depth == "comprehensive" else 5,
            )

            results["raw_sources"].extend(competitor_data.get("results", []))

            competitor_context = self.search_tool.format_results_for_llm(
                competitor_data
            )
            competitor_analysis = await self._analyze_competitors(
                company_name, competitor_context
            )
            results["competitors"] = competitor_analysis

            # 3. Market Trends (if industry provided)
            if industry:
                trend_data = await self.search_tool.get_market_trends(
                    industry=industry,
                    max_results=8 if research_depth == "comprehensive" else 4,
                )

                results["raw_sources"].extend(trend_data.get("results", []))

                trend_context = self.search_tool.format_results_for_llm(trend_data)
                trend_analysis = await self._analyze_trends(industry, trend_context)
                results["market_trends"] = trend_analysis

            logger.info(
                f"Research complete for {company_name}. "
                f"Processed {len(results['raw_sources'])} sources"
            )

            return results

        except Exception as e:
            logger.error(f"Research failed for {company_name}: {e}")
            raise

    async def _analyze_company(
        self,
        company_name: str,
        search_context: str,
    ) -> str:
        """Analyze company information from search results."""
        user_message = RESEARCHER_ANALYZE_COMPANY.format(
            company_name=company_name, search_context=search_context
        )
        return await self._invoke_llm(self._create_messages(user_message))

    async def _analyze_competitors(
        self,
        company_name: str,
        search_context: str,
    ) -> str:
        """Analyze competitor landscape."""
        user_message = RESEARCHER_ANALYZE_COMPETITORS.format(
            company_name=company_name, search_context=search_context
        )
        return await self._invoke_llm(self._create_messages(user_message))

    async def _analyze_trends(
        self,
        industry: str,
        search_context: str,
    ) -> str:
        """Analyze market trends."""
        user_message = RESEARCHER_ANALYZE_TRENDS.format(
            industry=industry, search_context=search_context
        )
        return await self._invoke_llm(self._create_messages(user_message))
