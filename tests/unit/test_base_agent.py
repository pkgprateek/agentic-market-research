"""Unit tests for base agent class."""

from unittest.mock import MagicMock, patch

import pytest

from src.agents.base import BaseAgent
from src.utils.cost_tracker import CostTracker


class MockAgent(BaseAgent):
    """Concrete test agent for testing base class."""

    def get_system_prompt(self) -> str:
        return "Test system prompt"

    async def run(self, **kwargs):
        return {"result": "test"}


@pytest.mark.asyncio
async def test_base_agent_initialization():
    """Test base agent initializes correctly."""
    tracker = CostTracker()

    with patch("src.agents.base.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(
            default_model="llama-3.3-70b-versatile",
            llm_api_key="test-key",
            llm_base_url="https://api.groq.com/openai/v1",
            llm_provider="groq",
        )

        agent = MockAgent(
            name="TestAgent",
            model="llama-3.1-8b-instant",
            temperature=0.5,
            cost_tracker=tracker,
        )

        assert agent.name == "TestAgent"
        assert agent.model_name == "llama-3.1-8b-instant"
        assert agent.cost_tracker == tracker


@pytest.mark.asyncio
async def test_base_agent_uses_default_model():
    """Test agent uses default model from config."""
    with patch("src.agents.base.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(
            default_model="llama-3.3-70b-versatile",
            llm_api_key="test-key",
            llm_base_url="https://api.groq.com/openai/v1",
            llm_provider="groq",
        )

        agent = MockAgent(name="TestAgent")

        assert agent.model_name == "llama-3.3-70b-versatile"


@pytest.mark.asyncio
async def test_create_messages():
    """Test message creation."""
    with patch("src.agents.base.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(
            default_model="test-model",
            llm_api_key="test-key",
            llm_base_url="https://test.com",
            llm_provider="groq",
        )

        agent = MockAgent(name="TestAgent")

        messages = agent._create_messages("test user message")

        assert len(messages) == 2
        assert messages[0].content == "Test system prompt"
        assert messages[1].content == "test user message"


@pytest.mark.asyncio
async def test_get_cost_summary():
    """Test cost summary retrieval."""
    tracker = CostTracker()

    with patch("src.agents.base.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(
            default_model="test-model",
            llm_api_key="test-key",
            llm_base_url="https://test.com",
            llm_provider="groq",
        )

        agent = MockAgent(name="TestAgent", cost_tracker=tracker)

        # Track some usage
        tracker.track_usage("llama-3.3-70b-versatile", 1000, 500)

        summary = agent.get_cost_summary()

        assert summary["total_input_tokens"] == 1000
        assert summary["total_output_tokens"] == 500
        assert summary["calls"] == 1
