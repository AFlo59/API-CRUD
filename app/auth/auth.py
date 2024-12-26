from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from app.auth.security import create_access_token, verify_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

# Endpoint pour générer un token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Exemple d'identifiants en dur ("admin"/"admin")
    if form_data.username == "admin" and form_data.password == "admin":
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.get("sub")  # Ex: "admin"
