from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    env: str = "development"
    api_version: str = "v0.1.0"
    database_url: str = "sqlite:///./searchtrust.db"
    ml_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
