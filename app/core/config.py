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
    WHATSAPP_ACCESS_TOKEN: str = "EAANq4X4WECkBOyU5SiCNLUMjFRqd6Cb3rvAz91UcHZAHFiC2M8gtUD3mLUmT7yt2RErITZCzJ9Tio4vwVMH4xq5zaG4ffXvrag08bHG87HJlIeySgVEQ2EjVpa4oo5eCjqlZB9lM1hBJk2sjoZCmiTHx5gFbBxtGchH5kTZBYtiLCFI9GOL7XYC0O1rBm6jl2dUZC24nRd2Hdq8tw13ZCLOr6DQJSoZD"
    WHATSAPP_PHONE_NUMBER_ID: str = "450374314817408"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()