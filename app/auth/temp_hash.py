from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hache un mot de passe.
    """
    return pwd_context.hash(password)

if __name__ == "__main__":
    plain_password = os.getenv("PASSWORD", "default_password")  # On récupère le mot de passe de l'env
    hashed = hash_password(plain_password)
    print(f"Mot de passe haché : {hashed}")
