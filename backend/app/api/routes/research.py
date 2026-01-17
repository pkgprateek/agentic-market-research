from fastapi import APIRouter

from app.models.research import (
    ResearchType,
    CompanyAnalysisRequest,
    CompetitiveComparisonRequest,
    ResearchResponse,
)

router = APIRouter()


@router.post("/research/company", response_model=ResearchResponse)
async def create_company_analysis(request: CompanyAnalysisRequest) -> ResearchResponse:
    """
    Create a company analysis report.

    This endpoint initiates research on a single company,
    returning a comprehensive analysis including SWOT,
    market position, and strategic recommendations.
    """
    # TODO: Implement actual research logic
    return ResearchResponse(
        id="placeholder",
        research_type=ResearchType.COMPANY_ANALYSIS,
        status="pending",
        company_name=request.company_name,
    )


@router.post("/research/comparison", response_model=ResearchResponse)
async def create_competitive_comparison(
    request: CompetitiveComparisonRequest,
) -> ResearchResponse:
    """
    Create a competitive comparison report.

    This endpoint initiates research comparing multiple companies,
    returning a side-by-side analysis with comparison matrices.
    """
    # TODO: Implement actual research logic
    return ResearchResponse(
        id="placeholder",
        research_type=ResearchType.COMPETITIVE_COMPARISON,
        status="pending",
        company_name=request.your_company,
    )


@router.get("/research/{research_id}", response_model=ResearchResponse)
async def get_research_status(research_id: str) -> ResearchResponse:
    """Get the status and results of a research request."""
    # TODO: Implement actual lookup logic
    return ResearchResponse(
        id=research_id,
        research_type=ResearchType.COMPANY_ANALYSIS,
        status="pending",
        company_name="placeholder",
    )
