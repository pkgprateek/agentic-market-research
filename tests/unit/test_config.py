"""Unit tests for configuration management.

These tests create Settings instances directly with explicit values
to avoid interference from the .env file.
"""

import pytest

from src.utils.config import Settings


def test_settings_with_groq():
    """Test settings with Groq API key."""
    settings = Settings(
        groq_api_key="test-groq-key",
        tavily_api_key="test-tavily-key",
        environment="production",
        _env_file=None,  # Disable .env file loading
    )

    assert settings.groq_api_key == "test-groq-key"
    assert settings.tavily_api_key == "test-tavily-key"
    assert settings.llm_provider == "groq"
    assert settings.llm_base_url == "https://api.groq.com/openai/v1"
    assert settings.is_production is True


def test_settings_with_openrouter():
    """Test settings with OpenRouter API key (Groq not set)."""
    settings = Settings(
        openrouter_api_key="test-openrouter-key",
        tavily_api_key="test-tavily-key",
        _env_file=None,
    )

    assert settings.openrouter_api_key == "test-openrouter-key"
    assert settings.llm_provider == "openrouter"
    assert settings.llm_base_url == "https://openrouter.ai/api/v1"


def test_settings_with_defaults():
    """Test settings use defaults for optional fields."""
    settings = Settings(
        groq_api_key="test-key",
        tavily_api_key="test-key",
        _env_file=None,
    )

    assert settings.default_model == "llama-3.3-70b-versatile"
    assert settings.max_cost_per_run == 2.0
    assert settings.langchain_project == "market-intelligence"


def test_settings_with_missing_llm_key():
    """Test settings raise error when no LLM key configured."""
    settings = Settings(
        tavily_api_key="test-tavily",
        _env_file=None,
    )

    with pytest.raises(ValueError, match="No LLM API key configured"):
        _ = settings.llm_provider


def test_is_production_property():
    """Test is_production property works correctly."""
    # Test development (default)
    settings = Settings(
        groq_api_key="test",
        tavily_api_key="test",
        environment="development",
        _env_file=None,
    )
    assert settings.is_production is False

    # Test production
    settings = Settings(
        groq_api_key="test",
        tavily_api_key="test",
        environment="production",
        _env_file=None,
    )
    assert settings.is_production is True
