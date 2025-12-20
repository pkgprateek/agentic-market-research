"""State definitions for LangGraph workflow."""

from typing import Annotated, Any, Dict, List, Literal, TypedDict, Union
import operator


class ResearchOutput(TypedDict):
    """Output structure for Research Agent."""

    company_name: str
    industry: Union[str, None]
    company_overview: str
    competitors: str
    market_trends: str
    raw_sources: List[Any]


class AnalysisOutput(TypedDict):
    """Output structure for Analysis Agent."""

    company_name: str
    swot: str
    competitive_matrix: str
    positioning: str
    strategic_recommendations: str


class ReportOutput(TypedDict):
    """Output structure for Writer Agent."""

    executive_summary: str
    full_report: str
    metadata: Dict[str, Any]


class IntelligenceState(TypedDict):
    """
    State for market intelligence workflow.

    This state is passed between agents and persisted across checkpoints.
    """

    # Input
    company_name: str
    industry: Union[str, None]
    research_depth: str  # "basic" or "comprehensive"

    # Research phase outputs
    research_data: ResearchOutput
    competitors: str  # Markdown string from analysis
    market_trends: str  # Markdown string from analysis
    raw_sources: List[Any]

    # Analysis phase outputs
    swot: str
    competitive_matrix: str
    positioning: str
    strategic_recommendations: str

    # Writing phase outputs
    executive_summary: str
    full_report: str
    report_metadata: Dict[str, Any]

    # Workflow metadata
    current_agent: Literal["research", "analysis", "writing", "human_review", "done"]
    iteration: int
    total_cost: float
    total_tokens: int
    errors: Annotated[List[str], operator.add]  # Accumulate errors across nodes

    # Human-in-the-loop
    human_feedback: Union[str, None]
    approved: bool
    revision_count: int
