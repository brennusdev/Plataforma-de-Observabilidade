from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Observability Platform"
    database_url: str = (
        "postgresql+psycopg://observability:observability@db:5432/observability"
    )
    collect_interval_seconds: int = 15

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
