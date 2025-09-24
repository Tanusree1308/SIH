# backend/config.py
# backend/config.py
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
# ... rest of the file ...

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
settings = Settings()