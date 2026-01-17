from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    openai_api_key: str = ""
    tavily_api_key: str = ""

    # Application
    environment: str = "development"
    debug: bool = True

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Cost limits
    max_cost_per_run: float = 2.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
