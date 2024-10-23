from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings class
    """

    APP_NAME: str = "Authentication Service API"
    SECRET_KEY: str = "very_secret"

    LOG_LEVEL: str = "INFO"


    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()