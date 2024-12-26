from sqlmodel import create_engine, Session
from app.config import settings
import logging

# Configurer le moteur
engine = create_engine(settings.database_url, echo=False)

# Logger
logger = logging.getLogger(__name__)

def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Erreur de session: {e}")
        raise

def check_database_connection():
    try:
        with Session(engine) as session:
            session.execute("SELECT 1")
            logger.info("Connexion à la base réussie.")
    except Exception as e:
        logger.error(f"Connexion échouée: {e}")
        raise ValueError("Échec de connexion.")
