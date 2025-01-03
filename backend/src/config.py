"""Configuration Setting"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file='.env'
        extra="ignore"

Config = Settings()

