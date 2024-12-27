from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from app.auth.auth import authenticate_user, create_access_token
from app.config import settings

# Création de l'instance APIRouter
router = APIRouter()

# Modèle de données pour la requête de connexion
class LoginData(BaseModel):
    username: str
    password: str

@router.post("/token", tags=["Authentification"], summary="Obtenir un token d'accès")
async def login(data: LoginData):
    """
    Authentifie l'utilisateur et retourne un token d'accès.
    """
    print(f"DEBUG: Données reçues -> username: {data.username}, password: {data.password}")
    
    if not authenticate_user(data.username, data.password):
        print("Échec d'authentification dans /token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.username}, expires_delta=access_token_expires
    )
    print(f"Token généré avec succès pour {data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
