import os
from passlib.context import CryptContext
from app.auth.auth import verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """Hache un mot de passe en utilisant bcrypt."""
    try:
        return pwd_context.hash(plain_password)
    except Exception as e:
        raise ValueError(f"Erreur lors du hachage du mot de passe : {str(e)}")

if __name__ == "__main__":
    plain_password = os.getenv("PASSWORD")
    if not plain_password:
        raise ValueError("La variable PASSWORD est manquante dans .env")
    hashed_password = hash_password(plain_password)
    print(f"Mot de passe en clair : {plain_password}")
    print(f"Hachage généré : {hashed_password}")
    print(f"Vérification du hachage : {verify_password(plain_password, hashed_password)}")
