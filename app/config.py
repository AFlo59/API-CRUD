import os
from dotenv import load_dotenv, set_key
from passlib.context import CryptContext
import secrets

# Charger explicitement le fichier `.env`
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)
print(f"DEBUG: USERNAME depuis .env : {os.getenv('USERNAME')}")
print(f"DEBUG: PASSWORD depuis .env : {os.getenv('PASSWORD')}")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Settings:
    # JWT Config
    SECRET_KEY = os.getenv("SECRET_KEY")
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
    USERNAME = os.getenv("USERNAME", "Admin")
    PASSWORD = os.getenv("PASSWORD", "Admin")
    HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")

    def __init__(self):
        self.validate_environment()

    def validate_environment(self):
        """
        Valide et met à jour dynamiquement les valeurs critiques pour l'application.
        """
        # Générer une nouvelle SECRET_KEY si elle n'existe pas ou est vide
        if not self.SECRET_KEY or self.SECRET_KEY.strip() == "":
            self.SECRET_KEY = secrets.token_urlsafe(32)
            set_key(env_path, "SECRET_KEY", self.SECRET_KEY)
            print(f"INFO: Nouvelle SECRET_KEY générée : {self.SECRET_KEY}")

        # Générer le hash du mot de passe s'il n'existe pas ou est vide
        if not self.HASHED_PASSWORD or self.HASHED_PASSWORD.strip() == "":
            self.HASHED_PASSWORD = pwd_context.hash(self.PASSWORD)
            set_key(env_path, "HASHED_PASSWORD", self.HASHED_PASSWORD)
            print(f"INFO: Nouveau HASHED_PASSWORD généré : {self.HASHED_PASSWORD}")

        if not all([self.DB_SERVER, self.DB_NAME, self.DB_USER, self.DB_PASSWORD]):
            raise ValueError("Les paramètres de connexion à la base de données sont manquants.")

    @property
    def database_url(self):
        """
        Génère l'URL de connexion à la base de données.
        """
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/"
            f"{self.DB_NAME}?driver={self.ODBC_DRIVER.replace(' ', '+')}"
        )

# Instanciation des paramètres
settings = Settings()
