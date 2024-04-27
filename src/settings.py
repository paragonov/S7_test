import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
    DB_PATH: str = f"{BASE_DIR}/db.sqlite3"
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"


class PathSettings(BaseSettings):
    PATH_TO_FILES: str = f"{BASE_DIR}/ln/"
    PATH_TO_JSON_FILES: str = f"{BASE_DIR}/src/tmp/out/"
    PATH_TO_OK: str = f"{BASE_DIR}/src/tmp/ok/"
    PATH_TO_ERR: str = f"{BASE_DIR}/src/tmp/err/"


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    file_paths: PathSettings = PathSettings()
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "")
    DEBUG: bool = not bool(ENVIRONMENT)
    SCHEDULE_TIME: int = 120


settings = Settings()
