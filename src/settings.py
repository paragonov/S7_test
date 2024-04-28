import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    TEST_DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db-test.sqlite3"


class PathSettings(BaseSettings):
    PATH_TO_LN: str = f"{BASE_DIR}/src/tmp/ln/"
    PATH_TO_OUT: str = f"{BASE_DIR}/src/tmp/out/"
    PATH_TO_OK: str = f"{BASE_DIR}/src/tmp/ok/"
    PATH_TO_ERR: str = f"{BASE_DIR}/src/tmp/err/"
    PATH_TO_TEST_FILE: str = f"{BASE_DIR}/src/tests/20221129_1223_DME.csv"


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    file_paths: PathSettings = PathSettings()
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "")
    DEBUG: bool = not bool(ENVIRONMENT)
    SCHEDULE_TIME: int = 120


settings = Settings()
