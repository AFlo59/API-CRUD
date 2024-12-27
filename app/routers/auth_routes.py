from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth.auth import authenticate_user, create_access_token
from app.config import settings

router = APIRouter()

@router.post("/token", tags=["Authentification"], summary="Obtenir un token d'accès")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie l'utilisateur et retourne un token d'accès.
    """
    if not authenticate_user(form_data.username, form_data.password):
        print("Échec d'authentification dans /token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    print(f"Token généré avec succès pour {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

