"""
Application configuration.

Loads all settings from environment variables using Pydantic BaseSettings.
Provides typed, validated access to database URL, JWT secrets, CORS origins,
and other configuration values across the application.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import json


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Reads from a .env file in the backend directory if present.
    All values can be overridden by setting the corresponding
    environment variable.
    """

    # ── Application ──────────────────────────────────────────────────────
    app_name: str = Field(default="AI Localization Engine")
    app_version: str = Field(default="0.1.0")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)

    # ── Server ───────────────────────────────────────────────────────────
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # ── Database ─────────────────────────────────────────────────────────
    database_url: str = Field(
        default="mysql+pymysql://root:password@127.0.0.1:3306/localization_engine"
    )
    db_pool_size: int = Field(default=5)
    db_max_overflow: int = Field(default=10)
    db_pool_timeout: int = Field(default=30)
    db_pool_recycle: int = Field(default=1800)

    # ── JWT Authentication ───────────────────────────────────────────────
    jwt_secret_key: str = Field(default="your-super-secret-key-change-in-production")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # ── CORS ─────────────────────────────────────────────────────────────
    cors_origins: str = Field(
        default='["http://localhost:3000","http://localhost:5173"]'
    )

    @property
    def cors_origin_list(self) -> List[str]:
        """Parse CORS origins from JSON string to list."""
        try:
            return json.loads(self.cors_origins)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:3000"]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# ── Singleton ────────────────────────────────────────────────────────────────
# Create a single settings instance to be imported across the application.

settings = Settings()
