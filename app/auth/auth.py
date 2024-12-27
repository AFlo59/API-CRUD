from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> bool:
    """
    Authentifie l'utilisateur en vérifiant le nom d'utilisateur et le mot de passe à partir des variables d'environnement.
    """
    print(f"DEBUG: USERNAME attendu (depuis .env) : {settings.USERNAME}")
    print(f"DEBUG: Nom d'utilisateur reçu : {username}")

    # Vérification du nom d'utilisateur
    if username != settings.USERNAME:
        print("Échec d'authentification : utilisateur non valide")
        return False

    # Vérification du mot de passe
    print(f"DEBUG: Mot de passe reçu : {password}")
    if not verify_password(password, settings.HASHED_PASSWORD):
        print("Échec d'authentification : mot de passe incorrect")
        return False

    print("Authentification réussie")
    return True




def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur invalide")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expiré")
    return {"username": username}
