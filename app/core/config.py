from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "Penny Wise - Grocery Tracker"

    # JWT
    secret_key: str = "your-secret-key-for-development-only"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_type: str = "sqlite"  # sqlite or mongodb
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "pennywise"

    # External APIs
    gemini_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
