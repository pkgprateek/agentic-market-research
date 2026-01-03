"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add project root to Python path for src imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for tests that need LLM config.

    Note: Not autouse - only use where explicitly needed.
    Config tests bypass this to test specific scenarios.
    """
    monkeypatch.setenv("GROQ_API_KEY", "gsk-mock-key")
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-mock-key")
    monkeypatch.setenv("LANGCHAIN_TRACING", "false")
    monkeypatch.setenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
