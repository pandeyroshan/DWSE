from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DWSE"
    APP_VERSION: str ="1.0.0"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/dwse_db"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    RABBITMQ_DEFAULT_USER: str = "guest"
    RABBITMQ_DEFAULT_PASS: str = "guest"

settings = Settings()
