"""Unit tests for workflow types."""

from src.workflows.types import IntelligenceState, ResearchType


class TestResearchType:
    """Tests for ResearchType enum."""

    def test_has_six_values(self) -> None:
        """Verify all research types are defined."""
        assert len(ResearchType) == 6

    def test_values_are_snake_case_strings(self) -> None:
        """Verify enum values use snake_case naming."""
        for rt in ResearchType:
            assert isinstance(rt.value, str)
            assert rt.value.islower()
            # All have underscores except none (all current ones do)
            assert "_" in rt.value

    def test_string_serialization(self) -> None:
        """Verify enum inherits from str for JSON compatibility."""
        rt = ResearchType.COMPANY_ANALYSIS
        assert str(rt) == "ResearchType.COMPANY_ANALYSIS"
        assert rt.value == "company_analysis"
        # Can be used as dict key and serialized
        assert rt == "company_analysis"

    def test_enum_members(self) -> None:
        """Verify expected enum members exist."""
        expected = [
            "COMPANY_ANALYSIS",
            "COMPETITIVE_COMPARISON",
            "MARKET_LANDSCAPE",
            "BATTLE_CARD",
            "INVESTMENT_THESIS",
            "CUSTOM_QUERY",
        ]
        actual = [member.name for member in ResearchType]
        assert actual == expected


class TestIntelligenceState:
    """Tests for IntelligenceState TypedDict."""

    def test_includes_research_type(self) -> None:
        """Verify state schema includes research_type field."""
        assert "research_type" in IntelligenceState.__annotations__

    def test_has_all_required_fields(self) -> None:
        """Verify state schema has all expected fields."""
        required_fields = [
            "research_type",
            "company_name",
            "industry",
            "research_depth",
            "research_data",
            "competitors",
            "market_trends",
            "raw_sources",
            "swot",
            "competitive_matrix",
            "positioning",
            "strategic_recommendations",
            "executive_summary",
            "full_report",
            "report_metadata",
            "current_agent",
            "iteration",
            "total_cost",
            "total_tokens",
            "errors",
            "human_feedback",
            "approved",
            "revision_count",
        ]

        annotations = IntelligenceState.__annotations__
        for field in required_fields:
            assert field in annotations, f"Missing field: {field}"
