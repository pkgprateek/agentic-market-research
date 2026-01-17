from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    groq_api_key: str = ""
    openrouter_api_key: str = ""
    tavily_api_key: str = ""

    # Model Configuration
    default_model: str = "openai/gpt-oss-120b"

    # Application
    environment: str = "development"
    debug: bool = True

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Cost limits
    max_cost_per_run: float = 2.0

    @property
    def llm_api_key(self) -> str:
        """Return the active LLM API key (Groq preferred, fallback to OpenRouter)."""
        return self.groq_api_key or self.openrouter_api_key

    @property
    def llm_provider(self) -> str:
        """Return the active LLM provider name."""
        if self.groq_api_key:
            return "groq"
        elif self.openrouter_api_key:
            return "openrouter"
        return "none"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
