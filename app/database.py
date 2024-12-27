from sqlmodel import create_engine, Session
from app.config import settings
import logging

# Crée l'engine de connexion à la base de données
engine = create_engine(
    settings.database_url,
    echo=False  # Suppression de la référence à app_name
)

# Configure le logger pour capturer les erreurs éventuelles
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_session():
    """
    Gère la création et la fermeture de la session de base de données.

    Utilise le contexte de gestion de session pour garantir la fermeture correcte
    de la session même en cas d'exception.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Erreur lors de la gestion de la session de base de données : {str(e)}")
        raise

# Vérification de la connexion à la base de données
def check_database_connection():
    """Vérifie la connexion à la base de données"""
    try:
        with Session(engine) as session:
            session.execute("SELECT 1")
            logger.info("Connexion à la base de données réussie.")
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données : {str(e)}")
        raise ValueError("Échec de la connexion à la base de données. Vérifiez la configuration.")
