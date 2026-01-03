"""Configuration management using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # === LLM Providers ===
    # Groq (primary - fast inference)
    groq_api_key: str | None = Field(None, description="Groq API key")

    # OpenRouter (secondary - 400+ models)
    openrouter_api_key: str | None = Field(None, description="OpenRouter API key")

    # === Search APIs ===
    tavily_api_key: str = Field(..., description="Tavily API key for web search")

    # === Observability ===
    langsmith_api_key: str | None = Field(None, description="LangSmith API key")
    langchain_tracing: bool = Field(False, description="Enable LangChain tracing")
    langchain_project: str = Field("market-intelligence", description="LangSmith project")

    # === Application Settings ===
    environment: str = Field("development", description="development or production")
    default_model: str = Field(
        "llama-3.3-70b-versatile",
        description="Default LLM model",
    )
    max_cost_per_run: float = Field(2.0, description="Max cost per run (USD)")

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"

    @property
    def llm_provider(self) -> str:
        """Determine which LLM provider to use based on available keys."""
        if self.groq_api_key:
            return "groq"
        elif self.openrouter_api_key:
            return "openrouter"
        else:
            raise ValueError("No LLM API key configured. Set GROQ_API_KEY or OPENROUTER_API_KEY")

    @property
    def llm_api_key(self) -> str:
        """Get the active LLM API key."""
        if self.groq_api_key:
            return self.groq_api_key
        elif self.openrouter_api_key:
            return self.openrouter_api_key
        else:
            raise ValueError("No LLM API key configured")

    @property
    def llm_base_url(self) -> str:
        """Get the LLM API base URL based on provider."""
        if self.groq_api_key:
            return "https://api.groq.com/openai/v1"
        else:
            return "https://openrouter.ai/api/v1"


def get_settings() -> Settings:
    """Get settings instance (lazy-loaded)."""
    return Settings()  # type: ignore[call-arg]
