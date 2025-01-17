"""Configuration Setting"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    DESC: str
    API_VERSION: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        extra = "ignore"


Config = Settings()
