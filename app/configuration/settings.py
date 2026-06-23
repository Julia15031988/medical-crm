from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY_ACCESS: str
    SECRET_KEY_REFRESH: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
