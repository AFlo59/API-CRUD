from pydantic_settings import BaseSettings
from passlib.context import CryptContext
import os
import secrets
from dotenv import load_dotenv

# Charger explicitement le fichier `.env` à la racine
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Settings(BaseSettings):
    # JWT Config
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Database Config
    DB_SERVER: str = os.getenv("DB_SERVER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_PORT: int = int(os.getenv("DB_PORT", 1433))
    ODBC_DRIVER: str = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    # Authentication
    USERNAME: str = os.getenv("USERNAME", "default_user")
    PASSWORD: str = os.getenv("PASSWORD", "default_password")
    HASHED_PASSWORD: str = os.getenv("HASHED_PASSWORD", "")

    def validate_and_hash_password(self):
        """
        Si le mot de passe haché est vide, on le génère à partir du mot de passe en clair.
        """
        if not self.HASHED_PASSWORD:
            self.HASHED_PASSWORD = pwd_context.hash(self.PASSWORD)

settings = Settings()
settings.validate_and_hash_password()
