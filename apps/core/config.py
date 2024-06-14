from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ModelConfigBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_ignore_empty=True,
        extra="ignore"
    )


class EnvironmentSettings(ModelConfigBaseSettings):
    DEBUG: bool
    SERVER_HOST: str
    SERVER_PORT: int
    API_VERSION: str

    @computed_field
    @property
    def API_PREFIX(self) -> str:
        return f"/api/{self.API_VERSION}"


class AuthenticationSettings(ModelConfigBaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str


class DatabaseSettings(ModelConfigBaseSettings):     # db
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    @computed_field
    @property
    # https://stackoverflow.com/questions/71789778/modulenotfounderror-no-module-named-psycopg2-by-using-pyodide
    def DB_URI(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(ModelConfigBaseSettings):
    environment: EnvironmentSettings = EnvironmentSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
