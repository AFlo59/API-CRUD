import os
from dotenv import load_dotenv, set_key
from passlib.context import CryptContext
import secrets

# Charger explicitement le fichier `.env`
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def update_env_file(key: str, value: str):
    """Met à jour ou ajoute une clé dans le fichier .env."""
    with open(env_path, "r") as file:
        lines = file.readlines()

    key_found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_found = True
            break

    if not key_found:
        lines.append(f"{key}={value}\n")

    with open(env_path, "w") as file:
        file.writelines(lines)


def reload_env():
    """Recharge les variables d'environnement après mise à jour."""
    load_dotenv(dotenv_path=env_path, override=True)
    print("INFO: Variables d'environnement rechargées.")


class Settings:
    # JWT Config
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    # Configuration de la base de données
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = int(os.getenv("DB_PORT", 1433))
    ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    # Authentification
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")

    def __init__(self):
        self.validate_environment()

    def validate_environment(self):
        """Valide et met à jour dynamiquement les valeurs critiques pour l'application."""
        # Générer une nouvelle SECRET_KEY si elle n'existe pas ou est vide
        if not self.SECRET_KEY or self.SECRET_KEY.strip() == "":
            self.SECRET_KEY = secrets.token_urlsafe(32)
            update_env_file("SECRET_KEY", self.SECRET_KEY)
            print(f"INFO: Nouvelle SECRET_KEY générée : {self.SECRET_KEY}")

        # Générer le hash du mot de passe s'il n'existe pas ou est vide
        self._update_password_hash()

        if not all([self.DB_SERVER, self.DB_NAME, self.DB_USER, self.DB_PASSWORD]):
            raise ValueError("Les paramètres de connexion à la base de données sont manquants.")

    def _update_password_hash(self):
        """Génère un nouveau hash si le mot de passe a changé ou si le hash est absent."""
        if not self.HASHED_PASSWORD or not pwd_context.verify(self.PASSWORD, self.HASHED_PASSWORD):
            self.HASHED_PASSWORD = pwd_context.hash(self.PASSWORD)
            update_env_file("HASHED_PASSWORD", self.HASHED_PASSWORD)
            print("INFO: Nouveau HASHED_PASSWORD généré.")

    def reload_critical_values(self):
        """Recharge les valeurs critiques après mise à jour de l'environnement."""
        self.USERNAME = os.getenv("USERNAME")
        self.PASSWORD = os.getenv("PASSWORD")
        self.HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")
        self._update_password_hash()

    @property
    def database_url(self):
        """Génère l'URL de connexion à la base de données."""
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/"
            f"{self.DB_NAME}?driver={self.ODBC_DRIVER.replace(' ', '+')}&Encrypt=YES&TrustServerCertificate=YES"
        )


# Instanciation des paramètres
settings = Settings()
