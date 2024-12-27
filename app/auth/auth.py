from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.security import create_access_token, verify_password
from app.config import settings

router = APIRouter()

@router.post("/token", tags=["Authentification"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie un utilisateur et génère un token JWT.
    """
    # Vérification du username et du mot de passe haché
    if form_data.username != settings.USERNAME or not verify_password(form_data.password, settings.HASHED_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Génération du token JWT
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
