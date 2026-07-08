import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BASE_DIR: Path = Path(__file__).parent.parent

    # --- Email templates ---
    PATH_TO_EMAIL_TEMPLATES_DIR: str = str(
        BASE_DIR / "email_notifications" / "templates"
    )
    ACTIVATION_EMAIL_TEMPLATE_NAME: str = "activation.html"
    ACTIVATION_COMPLETE_EMAIL_TEMPLATE_NAME: str = "activation_complete.html"
    PASSWORD_RESET_TEMPLATE_NAME: str = "password_reset.html"
    PASSWORD_RESET_COMPLETE_TEMPLATE_NAME: str = "password_reset_complete.html"
    PASSWORD_CHANGE_NAME: str = "password_change.html"

    APPOINTMENT_REMINDER_TEMPLATE_NAME: str = "appointment_reminder.html"
    LAB_RESULTS_TEMPLATE_NAME: str = "lab_results.html"
    INVOICE_TEMPLATE_NAME: str = "invoice.html"

    LOGIN_TIME_DAYS: int = 7

    # --- Email SMTP / MailHog ---
    EMAIL_HOST: str = "mailhog"
    EMAIL_PORT: int = 1025
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    EMAIL_USE_TLS: bool = False

    # --- Queue / Tasks ---
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # --- Storage / MinIO ---
    S3_STORAGE_HOST: str = "minio"
    S3_STORAGE_PORT: int = 9000
    S3_STORAGE_ACCESS_KEY: str = "minioadmin"
    S3_STORAGE_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "crm-storage"

    @property
    def S3_STORAGE_ENDPOINT(self) -> str:
        return f"http://{self.S3_STORAGE_HOST}:{self.S3_STORAGE_PORT}"


class Settings(BaseAppSettings):
    # --- Database ---
    POSTGRES_USER: str = "crm_user"
    POSTGRES_PASSWORD: str = "crm_password"
    POSTGRES_HOST: str = "db"
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: str = "medical_crm"

    # --- JWT ---
    SECRET_KEY_ACCESS: str = "change_me_access_secret"
    SECRET_KEY_REFRESH: str = "change_me_refresh_secret"
    JWT_SIGNING_ALGORITHM: str = "HS256"
    ALGORITHM: str = "HS256"

    # --- Token lifetimes ---
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ACTIVATION_TOKEN_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 2

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_DB_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return self.DATABASE_URL.replace(
            "postgresql+asyncpg",
            "postgresql+psycopg",
        )

class TestingSettings(BaseAppSettings):
    # --- Test DB ---
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # --- JWT ---
    SECRET_KEY_ACCESS: str = "test_access_secret"
    SECRET_KEY_REFRESH: str = "test_refresh_secret"
    JWT_SIGNING_ALGORITHM: str = "HS256"
    ALGORITHM: str = "HS256"

    # --- Token lifetimes ---
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ACTIVATION_TOKEN_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 2

    def model_post_init(self, __context: dict[str, Any] | None = None) -> None:
        object.__setattr__(self, "DATABASE_URL", "sqlite+aiosqlite:///./test.db")


@lru_cache
def get_settings() -> BaseAppSettings:
    if os.getenv("ENVIRONMENT", "local") == "testing":
        return TestingSettings()

    return Settings()


settings = get_settings()
