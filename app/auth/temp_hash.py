import os
from passlib.context import CryptContext
from auth.auth import verify_password

# Initialisation du contexte de hachage avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Hache un mot de passe en utilisant bcrypt.

    Args:
        plain_password (str): Le mot de passe en texte clair à hacher.

    Returns:
        str: Le mot de passe haché.
    """
    try:
        hashed_password = pwd_context.hash(plain_password)
        return hashed_password
    except Exception as e:
        # Gestion des erreurs pendant le hachage du mot de passe
        raise ValueError(f"Une erreur est survenue lors du hachage du mot de passe : {str(e)}")

if __name__ == "__main__":
    plain_password = os.getenv("PASSWORD")  # Utilise le mot de passe du fichier .env
    hashed_password = hash_password(plain_password)
    
    print(f"Mot de passe en clair : {plain_password}")
    print(f"Hachage généré : {hashed_password}")
    print(f"Vérification du hachage : {verify_password(plain_password, hashed_password)}")
