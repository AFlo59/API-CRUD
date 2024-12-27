import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import secrets

# Charger explicitement le fichier `.env` à la racine
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Settings:
    # JWT Config
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))  # Généré dynamiquement si vide
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Configuration de la base de données
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = int(os.getenv("DB_PORT", 1433))
    ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    # Authentification
    USERNAME = os.getenv("USERNAME", "default_user")
    PASSWORD = os.getenv("PASSWORD", "default_password")
    HASHED_PASSWORD = os.getenv("HASHED_PASSWORD", "")

    @property
    def database_url(self):
        """
        Générer dynamiquement l'URL de connexion à la base de données.
        """
        if not all([self.DB_SERVER, self.DB_NAME, self.DB_USER, self.DB_PASSWORD]):
            raise ValueError("Les paramètres de connexion à la base de données ne sont pas définis dans .env")
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/"
            f"{self.DB_NAME}?driver={self.ODBC_DRIVER.replace(' ', '+')}"
        )

    def validate_and_hash_password(self):
        """
        Si le mot de passe haché est vide, on le génère à partir du mot de passe en clair.
        """
        if not self.HASHED_PASSWORD:
            self.HASHED_PASSWORD = pwd_context.hash(self.PASSWORD)

# Créer une instance des paramètres
settings = Settings()
settings.validate_and_hash_password()
