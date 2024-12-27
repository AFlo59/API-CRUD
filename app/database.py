from sqlmodel import create_engine, Session
from app.config import settings
import logging

# Création de l'engine pour la base de données
engine = create_engine(settings.database_url, echo=False)

# Configurer le logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_session():
    """
    Gère la session de base de données.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Erreur de session DB : {str(e)}")
        raise

def check_database_connection():
    """
    Vérifie la connexion à la base de données.
    """
    try:
        with Session(engine) as session:
            session.execute("SELECT 1")
            logger.info("Connexion DB réussie.")
    except Exception as e:
        logger.error(f"Erreur de connexion DB : {str(e)}")
        raise ValueError("Connexion échouée.")
