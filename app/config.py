import os
from pydantic import BaseSettings, ValidationError

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_SERVER: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:1433/"
            f"{self.DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server"
        )

try:
    settings = Settings()
except ValidationError as e:
    raise ValueError(f"Configuration invalid: {e}")
