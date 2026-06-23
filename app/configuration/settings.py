from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY_ACCESS: str
    SECRET_KEY_REFRESH: str
    ALGORITHM: str = "HS256"

    # --- Tokens ---
    ACTIVATION_TOKEN_EXPIRE_HOURS: int = 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 2

    # --- Email ---
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_USE_TLS: bool = True
    PATH_TO_EMAIL_TEMPLATES_DIR: str = "app/templates/emails"
    ACTIVATION_EMAIL_TEMPLATE_NAME: str = "activation.html"
    ACTIVATION_COMPLETE_EMAIL_TEMPLATE_NAME: str = "activation_complete.html"
    PASSWORD_RESET_TEMPLATE_NAME: str = "password_reset.html"
    PASSWORD_RESET_COMPLETE_TEMPLATE_NAME: str = "password_reset_complete.html"
    SUCCESS_PAYMENT_TEMPLATE_NAME: str = "success_payment.html"

    class Config:
        env_file = ".env"

settings = Settings()

