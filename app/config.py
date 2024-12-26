import secrets
from pydantic_settings import BaseSettings
from pydantic import ValidationError

class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_SERVER: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 1433  # Port par défaut
    ODBC_DRIVER: str = "ODBC Driver 18 for SQL Server"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/"
            f"{self.DB_NAME}?driver={self.ODBC_DRIVER.replace(' ', '+')}"
        )

try:
    settings = Settings()
except ValidationError as e:
    raise ValueError(f"Configuration invalid: {e}")
