"""Research Agent for gathering market intelligence data.

Optimized with asyncio.gather for parallel search and analysis operations.
"""

import asyncio

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

    Uses asyncio.gather to parallelize:
    - Search queries (company + competitors + trends)
    - LLM analysis calls

    This provides ~3x speedup over sequential execution.
    """

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.3,  # Lower for more factual responses
        cost_tracker: CostTracker | None = None,
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
        industry: str | None = None,
        research_depth: str = "basic",
    ) -> ResearchOutput:
        """
        Gather research data about a company using parallel operations.

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
        logger.info(f"Starting parallel research for: {company_name}")

        max_results = 10 if research_depth == "comprehensive" else 5
        trend_results = 8 if research_depth == "comprehensive" else 4

        try:
            # Phase 1: Parallel search queries (I/O bound - huge speedup)
            search_tasks = [
                self.search_tool.get_company_info(company_name, max_results),
                self.search_tool.get_competitor_info(company_name, industry, max_results),
            ]

            # Only add trends search if industry is provided
            if industry:
                search_tasks.append(
                    self.search_tool.get_market_trends(industry, max_results=trend_results)
                )

            search_results = await asyncio.gather(*search_tasks)

            company_data = search_results[0]
            competitor_data = search_results[1]
            trend_data = search_results[2] if industry else {"results": []}

            # Collect all sources
            raw_sources: list = []
            raw_sources.extend(company_data.get("results", []))
            raw_sources.extend(competitor_data.get("results", []))
            raw_sources.extend(trend_data.get("results", []))

            # Phase 2: Parallel LLM analysis (CPU/API bound - significant speedup)
            company_context = self.search_tool.format_results_for_llm(company_data)
            competitor_context = self.search_tool.format_results_for_llm(competitor_data)
            trend_context = self.search_tool.format_results_for_llm(trend_data) if industry else ""

            analysis_tasks = [
                self._analyze_company(company_name, company_context),
                self._analyze_competitors(company_name, competitor_context),
            ]

            if industry:
                analysis_tasks.append(self._analyze_trends(industry, trend_context))

            analysis_results = await asyncio.gather(*analysis_tasks)

            company_analysis = analysis_results[0]
            competitor_analysis = analysis_results[1]
            trend_analysis = analysis_results[2] if industry else ""

            results: ResearchOutput = {
                "company_name": company_name,
                "industry": industry,
                "company_overview": company_analysis,
                "competitors": competitor_analysis,
                "market_trends": trend_analysis,
                "raw_sources": raw_sources,
            }

            logger.info(
                f"Research complete for {company_name}. Processed {len(raw_sources)} sources"
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
