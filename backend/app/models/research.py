from enum import Enum

from pydantic import BaseModel, Field


class ResearchType(str, Enum):
    """Types of research that can be performed."""

    COMPANY_ANALYSIS = "company_analysis"
    COMPETITIVE_COMPARISON = "competitive_comparison"


class FocusArea(str, Enum):
    """Focus areas for company analysis."""

    PRODUCTS_SERVICES = "products_services"
    PRICING = "pricing"
    LEADERSHIP = "leadership"
    FINANCIALS = "financials"
    MARKET_POSITION = "market_position"


class ComparisonDimension(str, Enum):
    """Dimensions for competitive comparison."""

    FEATURES = "features"
    PRICING = "pricing"
    MARKET_SHARE = "market_share"
    TECHNOLOGY = "technology"
    CUSTOMER_SEGMENTS = "customer_segments"


class CompanyAnalysisRequest(BaseModel):
    """Request model for company analysis."""

    company_name: str = Field(..., min_length=1, description="Name of the company to analyze")
    industry: str | None = Field(None, description="Industry (optional, will be inferred)")
    focus_areas: list[FocusArea] = Field(
        default_factory=lambda: list(FocusArea),
        description="Areas to focus the analysis on",
    )


class CompetitiveComparisonRequest(BaseModel):
    """Request model for competitive comparison."""

    your_company: str = Field(..., min_length=1, description="Your company name")
    competitors: list[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="List of competitor companies (1-5)",
    )
    comparison_dimensions: list[ComparisonDimension] = Field(
        default_factory=lambda: list(ComparisonDimension),
        description="Dimensions to compare",
    )


class ConfidenceLevel(str, Enum):
    """Confidence level for claims."""

    HIGH = "high"  # 90%+ confidence
    MEDIUM = "medium"  # 70-89% confidence
    LOW = "low"  # <70% confidence


class Source(BaseModel):
    """A source citation."""

    title: str
    url: str
    publication_date: str | None = None
    freshness: str | None = None  # fresh, recent, stale


class ResearchResponse(BaseModel):
    """Response model for research requests."""

    id: str
    research_type: ResearchType
    status: str  # pending, in_progress, completed, failed
    company_name: str
    report_markdown: str | None = None
    sources: list[Source] = Field(default_factory=list)
    intelligence_gaps: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    overall_confidence: ConfidenceLevel | None = None
