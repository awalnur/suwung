from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings class
    """

    APP_NAME: str = "Authentication Service API"
    SECRET_KEY: str = "very_secret"

    LOG_LEVEL: str = "INFO"

    ACCESS_TOKEN_EXPIRATION: int = 3600
    REFRESH_TOKEN_EXPIRATION: int = 86400
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()