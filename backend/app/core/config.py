"""Backend application configuration."""
import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    env: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ecgqi_db"

    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_url: str = "http://localhost:8000"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # File Upload
    upload_dir: str = "/tmp/ecgqi_uploads"
    max_upload_size_mb: int = 50
    allowed_extensions: list[str] = ["png", "jpg", "jpeg", "pdf"]

    # AI Service
    ai_service_type: str = "mock"
    ai_model_name: str = "ECG-Mock-v1"
    ai_model_version: str = "0.1.0"
    ai_confidence_threshold: float = 0.7

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Demo Data
    seed_demo_data: bool = True
    demo_password: str = "DemoPass123!"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False

    def get_database_url(self) -> str:
        """Return the database URL for SQLAlchemy."""
        return self.database_url

    @property
    def max_upload_size_bytes(self) -> int:
        """Convert max upload size to bytes."""
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
