from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Garita Tecnologica"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/garita_db"
    SECRET_KEY: str = "CAMBIAR_ESTA_CLAVE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720
    CORS_ORIGINS: str = "http://localhost:8080,http://127.0.0.1:8080,http://localhost:8000"
    EMAIL_MODE: str = "console"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "garita@residencial.local"
    FRONTEND_URL: str = "http://localhost:8080"
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
