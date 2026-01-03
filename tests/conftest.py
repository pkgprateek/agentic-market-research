"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add project root to Python path for src imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(autouse=True)
def mock_env(request, monkeypatch):
    """Mock environment variables for all tests.

    This ensures tests work in CI where no .env file exists.
    Tests marked with @pytest.mark.no_mock_env will skip this fixture.
    """
    # Skip for tests that need to control their own environment
    if request.node.get_closest_marker("no_mock_env"):
        return

    monkeypatch.setenv("GROQ_API_KEY", "gsk-mock-key")
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-mock-key")
    monkeypatch.setenv("LANGCHAIN_TRACING", "false")
    monkeypatch.setenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
